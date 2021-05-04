from flask import Flask,redirect,url_for
app = Flask(__name__)

@app.route('/admin')
def admin():
   return 'Hello Admin'

@app.route('/Guest/<guest>')
def guest(guest):
   return 'Hello %s as a guest' %guest

@app.route('/user/<name>')
def hello_user(name):
   if name == 'admin':
      return redirect(url_for('admin'))
   else:
      return redirect(url_for('guest', guest = name))

if __name__ == '__main__':
   app.run(debug=True)