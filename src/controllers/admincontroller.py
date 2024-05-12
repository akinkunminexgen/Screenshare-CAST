from flask import Blueprint, render_template, request, redirect, url_for, session, flash, Response, abort, send_from_directory, send_file
from jinja2 import TemplateNotFound
import os, sys, threading
from classes.AIACast import FFmpegCommandWithTimeLimit
from classes.AIARemake import TransformToExe
from classes.Pyinst import PyToExeConverter
from classes.getIP import NetworkUtils
from pathlib import Path

sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))
from src.models.User import User
from src.models.Ticket import Ticket
import time



adminctrl = Blueprint('admin', __name__)
user = User()
tickets = Ticket()
ip = NetworkUtils.get_local_ip()
ffmpeg = FFmpegCommandWithTimeLimit()
tranform = TransformToExe()
installer = PyToExeConverter('exec2.py')

destination_path = Path(f'./storage/scriptingexe/exec2.exe')
                


#Routing to the User upload page page for both GET and POST
@adminctrl.route('/', methods=['GET'])
def access_page():
    if 'username' in session:
        the_user = user.find_data(session['username'])
        return render_template('admin/index.html', user = the_user)
    else:
        return redirect(url_for('login.login_GET'))
    

@adminctrl.route('/user', methods=['POST'])
def uploadUser_POST():
    pass
        


@adminctrl.route('/', methods=['POST'])
def access_page_post():

    #checking if session exists
    if 'username' in session:
        if request.form['to_check'] == 'admin':

            if request.form['btn'] == "savebtn":

                if request.form['pin'] == "" or request.form['timer'] == "0":

                    flash('Generate a ticket!/Set timer')
                    return redirect(url_for('admin.access_page'))
                
                else:

                    ticket = tickets.fmt(request.form['pin'], request.form['timer'])
                    ticket = tickets.create(ticket)

                    
                    udpip = f"udp://{ip}:{request.form['pin']}"
                    ff = ffmpeg.exe_command_to_recieve(request.form['timer'], udpip)
                    
                    flash(ticket)
                    return redirect(url_for('admin.access_page'))
                
            elif request.form['btn'] == "startbtn":
                return 'startbtn'
            else:

                ffmpeg.killer()
                flash(f'Process Killed! ')
                
                return redirect(url_for('admin.access_page'))
        else:
            
            
            if ip == None:
                flash('Network connection issue!')
                return redirect(url_for('admin.access_page'))
                exit()
            
            if request.form['btn'] == 'startbtn':
                ticket = tickets.find_data(request.form['pin'])

                if ticket == None:

                    flash('That token is unavailable!')
                    return redirect(url_for('admin.access_page'))
                else:
                    msg = tranform.copy_file()
                    if msg != 'successful':                   
                        flash('There is an issue')
                        return redirect(url_for('admin.access_page'))
                        exit()
                    
                    udpip = f"udp://{ip}:{request.form['pin']}"
                    tranform.alter_file(ticket['timer'], udpip)

                    
                    try:
                        t1 = threading.Thread(target=installer.convert, args=(True, True))
                        t1.start()
                        time.sleep(7)
                        t1.join()

                        flash(f'Awesome!, Please double click on the downloaded file')
                        return send_file(destination_path, as_attachment=True)
                    except Exception as e:
                        abort(404, description="Resource not found")

            else:
                 try:
                     ffmpeg.killer_client()
                     flash(f'Process Killed!')
                     return redirect(url_for('admin.access_page'))
                 except FileNotFoundError:            
                    abort(404, description="Resource not found")
                
                
            
    else:
        return redirect(url_for('login.login_GET'))




    








    



