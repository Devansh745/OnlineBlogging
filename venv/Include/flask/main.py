from flask import Flask,render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime


with open('config.json','r') as c:
    params = json.load(c)["params"]
local_server = True

app = Flask(__name__)
app.secret_key = 'super-secret-key'
if local_server :
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)



class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    mes = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)

class Posts(db.Model):
    #sno,tittle,slug,content,date,imager_file
    sno = db.Column(db.Integer, primary_key=True)
    tittle = db.Column(db.String(70), nullable=False)
    slug = db.Column(db.String(12), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    imager_file = db.Column(db.String(12), nullable=True)


@app.route('/')
def home():
    posts = Posts.query.filter_by().all()[0:params['no_of_post']]
    return render_template('index.html', params = params, posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', params = params)

@app.route('/contact', methods = ['GET' , 'POST'])
def contact():
    # sno,name,email,phone_num,mes,date
    if request.method=='POST':
        name =  request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry =Contacts(name = name,email = email,phone_num= phone,mes = message,date = datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html', params = params)



@app.route('/post/<string:slug_post>', methods = ['GET'])
def post_rou(slug_post):
    post= Posts.query.filter_by(slug = slug_post).first()
    return render_template('post.html', params = params, post=post)

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():

    if 'user' in session and session['user'] == params['admin_user']:
        posts = Posts.query.all()
        return render_template('dashboard.html',params=params,posts= posts)

    if request.method=='POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if username == params['admin_user'] and userpass == params['admin_pass']:
            session['user'] = username
            posts = Posts.query.all()
            return render_template('dashboard.html',params=params,posts = posts)

    return render_template('login.html', params = params)

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/dashboard')

@app.route('/edit/<string:sno>', methods = ['GET','POST'])
def edit(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            title = request.form.get('tittle')
            slug= request.form.get('slug')
            content= request.form.get('content')
            ima_file= request.form.get('ima_file')
            if sno =='0':
                # sno,tittle,slug,content,date,imager_file
                post = Posts(tittle = title,slug=slug,content = content,date = datetime.now(),imager_file = ima_file)
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.tittle = title
                post.slug = slug
                post.content = content
                post.date = datetime.now()
                post.imager_file = ima_file
                db.session.commit()
                return redirect('/edit/'+sno)
    post =Posts.query.filter_by(sno=sno).first()
    return render_template('edit.html', params = params,post=post)


app.run(debug=True)