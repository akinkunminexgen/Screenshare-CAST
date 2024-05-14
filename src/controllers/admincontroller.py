from flask import Blueprint, render_template, request, redirect, url_for, session, flash, Response, abort, send_from_directory, send_file
from jinja2 import TemplateNotFound
import os, sys, threading, time
from classes.AIACast import FFmpegCommandWithTimeLimit
from classes.AIARemake import TransformToExe
from classes.Pyinst import PyToExeConverter
from classes.getIP import NetworkUtils
from pathlib import Path

sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))
from src.models.User import User
from src.models.Ticket import Ticket



adminctrl = Blueprint('admin', __name__)
user = User()
tickets = Ticket()
host_ip = NetworkUtils.get_local_ip()
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
    

        
@adminctrl.route('/', methods=['POST'])
def access_page_post():

    #checking if session exists
    if 'username' in session:
        #to ensure if it is admin or not
        if request.form['to_check'] == 'admin':
            #to determin which button was clicked
            if request.form['btn'] == "savebtn":

                if request.form['pin'] == "" or request.form['timer'] == "0":
                    #validating the form
                    flash('Generate a ticket!/Set timer')
                    return redirect(url_for('admin.access_page'))
                
                else:
                    #save ticket and timer to data.json
                    ticket = tickets.fmt(request.form['pin'], 
                                         request.form['timer'])
                    ticket = tickets.create(ticket)
                    
                    #appending the host ip with the ticket to create a socket
                    #and using udp protocol to recieve frame
                    udpip = f"udp://{host_ip}:{request.form['pin']}"
                    ff = ffmpeg.exe_command_to_recieve(request.form['timer'], 
                                                       udpip)                    
                    flash(f"{ff}")
                    return redirect(url_for('admin.access_page'))
                
            elif request.form['btn'] == "startbtn":
                if host_ip == "10.0.0.1741":
                    #if client is host, screen share should not execute
                    flash("This is the host! (session cannot be enabled!)")
                    return redirect(url_for('admin.access_page'))
                    exit()
                
                #ffplay listens on port 5555 anytime the admin wants to share
                udpip = f"udp://{host_ip}:5555"
                timers = "5"

                msg = tranform.copy_file()
                if msg != 'successful':                   
                        flash('There is an issue, (contact Admin)')
                        return redirect(url_for('admin.access_page'))
                        exit()
                    
                tranform.alter_file(timers, udpip)                    
                try:
                    t1 = threading.Thread(target=installer.convert, 
                                              args=(True, True))
                    t1.start()
                    #to give pyinstaller time to deploy the script to exe
                    time.sleep(12)
                    t1.join()

                    #enable the host to listen to udp @1234
                    ff = ffmpeg.exe_command_to_recieve(timers, 
                                                       udpip) 
                    flash(f'Awesome!, Please double click on the downloaded file')
                    return send_file(destination_path, as_attachment=True)
                except Exception as e:
                    abort(404, description="Resource not found")

            else:
                #kill the ffplay process
                ffmpeg.killer()
                #ffmpeg.killer_client()
                flash(f'Process Killed! ')                
                return redirect(url_for('admin.access_page'))
            
        else:            
            #check for ip
            if host_ip == None:
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
                        flash('There is an issue, (contact Admin)')
                        return redirect(url_for('admin.access_page'))
                        exit()
                    
                    udpip = f"udp://{host_ip}:{request.form['pin']}"
                    tranform.alter_file(ticket['timer'], udpip)

                    
                    try:
                        t1 = threading.Thread(target=installer.convert, 
                                              args=(True, True))
                        t1.start()
                        #to give pyinstaller time to deploy the script to .exe
                        time.sleep(12)
                        t1.join()

                        flash(f'Awesome! Pls double click on the downloaded file')
                        return send_file(destination_path, as_attachment=True)
                    except Exception as e:
                        abort(404, description="Resource not found")

            else:
                 try:
                     ffmpeg.killer()
                     flash(f'Process Killed! Close the exe2 file')
                     return redirect(url_for('admin.access_page'))
                 except FileNotFoundError:            
                    abort(404, description="Resource not found")
                
                
            
    else:
        return redirect(url_for('login.login_GET'))




    








    



