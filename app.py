from flask import Flask, render_template, redirect, session, url_for
from src.controllers.logincontroller import loginctrl
from src.controllers.admincontroller import adminctrl


app = Flask(__name__)
# Set the secret key to some random bytes.
app.secret_key = 'any random string'

@app.route("/")
def hello_world():
    return redirect(url_for('login.login_GET'))

#this route deletes all session stored during usage
@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username')
    if 'firstname' in session:
        session.pop('firstname')
    return redirect(url_for('login.login_GET'))

#by using bluepring, it is mandatory you register it to you app route
app.register_blueprint(loginctrl, url_prefix='/login')
app.register_blueprint(adminctrl, url_prefix='/admin')
 
if __name__ == '__main__':
   app.run(host='0.0.0.0', port="5000")


