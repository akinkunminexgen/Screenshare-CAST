from flask import Blueprint, render_template, abort, request, redirect, url_for, session, flash
from jinja2 import TemplateNotFound
from flask_bcrypt import check_password_hash
import os, sys

sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))
from src.models.User import User



loginctrl = Blueprint('login', __name__)

@loginctrl.route('/', methods=['GET'])
def login_GET():
    if 'username' in session:
        return redirect(url_for('admin.access_page'))
    else:
        return render_template('login/index.html')



@loginctrl.route('/', methods=['POST'])
def login_POST():
    #To make sure it's only post method that can execute this route
    if request.method == 'POST':
        #creating an instance of user
        the_user = User()

        #using the user class to get a return method
        login_user = the_user.find_data(request.form['username'])        

        if login_user != None:
            #creating a session for the application
            session['username'] = request.form['username']

            #compare if hashed password is the same
            if check_password_hash(login_user['password'],
                                    request.form['password']):
                
                #create a session for the name to be used across the app
                session['firstname'] = login_user['Firstname']
                #redirect to admin page if user is admin
                return redirect(url_for('admin.access_page'))
            else:
                #sending a session to the html page
                flash('Wrong Username/Password')
                session.pop('username')
                return redirect(url_for('login.login_GET') )
        else:
            #sending a session to the html page
            flash('Wrong Username/Password')
            return redirect(url_for('login.login_GET') )

@loginctrl.route('/<page>')
def show(page):
    try:
        return render_template(f'login/{page}.html')
    except TemplateNotFound:
        abort(404)
