from flask import Blueprint, render_template, request, redirect, url_for, session, flash, Response, abort, send_from_directory, send_file
from jinja2 import TemplateNotFound
from flask_bcrypt import generate_password_hash
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
installer = PyToExeConverter('esharexe22.py')

destination_path = Path(f'./storage/scriptingexe/esharexe22.exe')
                


#Routing to the User upload page page for both GET and POST
@adminctrl.route('', methods=['GET'])
def access_page():
    if 'username' in session:
        the_user = user.find_data(session['username'])
        return render_template('admin/index.html', user = the_user)
    else:
        return redirect(url_for('login.login_GET'))  

        
@adminctrl.route('', methods=['POST'])
def access_page_post():

    #checking if session exists
    if 'username' in session:
        #to ensure if it is admin or not
        if request.form['to_check'] == 'admin':
            #to determin which button was clicked
            if request.form['btn'] == "savebtn":

                if request.form['pin'] == "" or request.form['timer'] == "0":
                    #validating the form
                    flash('Generate a ticket!/Set timer', 'error')
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
                    flash(f"{ff}", 'success')
                    return redirect(url_for('admin.access_page'))
                
            elif request.form['btn'] == "startbtn":
                if host_ip == "10.0.0.1741gvdg":
                    #if client is host, screen share should not execute
                    flash("This is the host! (session cannot be enabled!)")
                    return redirect(url_for('admin.access_page'))
                    exit()
                
                #ffplay listens on port 5555 anytime the admin wants to share
                udpip = f"udp://{host_ip}:4444"
                timers = "5"

                msg = tranform.copy_file()
                if msg != 'successful':                   
                        flash('There is an issue, (contact Admin)', 'error')
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
                    
                    return send_file(destination_path, as_attachment=True)
                except Exception as e:
                    abort(404, description="Resource not found")

            else:
                #kill the ffplay process
                ffmpeg.killer()
                #ffmpeg.killer_client()
                flash(f'Process Killed!', 'success')                
                return redirect(url_for('admin.access_page'))
            
        else:            
            #check for ip
            if host_ip == None:
                flash('Network connection issue!', 'warning')
                return redirect(url_for('admin.access_page'))
                exit()
            
            if request.form['btn'] == 'startbtn':
                ticket = tickets.find_data(request.form['pin'])

                if ticket == None:

                    flash('That token is unavailable!', 'warning')
                    return redirect(url_for('admin.access_page'))
                else:
                    msg = tranform.copy_file()
                    if msg != 'successful':                   
                        flash('There is an issue, (contact Admin)', 'error')
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

                        ticket = tickets.delete_data(request.form['pin'])

                        return send_file(destination_path, as_attachment=True)
                    except Exception as e:
                        abort(404, description="Resource not found")

            else:
                 try:
                     ffmpeg.killer()
                     flash(f'Process Killed! Close the exe2 file', 'success')
                     return redirect(url_for('admin.access_page'))
                 except FileNotFoundError:            
                    abort(404, description="Resource not found")
                
                
            
    else:
        return redirect(url_for('login.login_GET'))




@adminctrl.route('/user')
def user_page():
    if 'username' in session:
        admin = user.find_data(session['username'])
        #not grant permission for ordinary user
        if admin['role'].lower() != 'admin':
            flash("Permission denied!", "error")
            return redirect(url_for('admin.access_page'))
            exit()        
        
        all_user = user.get_data()
        return render_template('admin/user.html', user = admin, 
                               others = all_user)
    else:
        return redirect(url_for('login.login_GET'))


@adminctrl.route('/add', methods=['GET'])
def add_user():
    if 'username' in session:
        the_user = user.find_data(session['username'])
        return render_template('admin/useradd.html', user = the_user)
    else:
        return redirect(url_for('login.login_GET'))
    

@adminctrl.route('/add', methods=['POST'])
def add_user_post():
    
    password = generate_password_hash(request.form['password']).decode('utf-8')

    dictn ={request.form['Username'] : {
       "Firstname": request.form['Firstname'],
        "Lastname": request.form['Lastname'],
        "sex": request.form['gender'],
        "password": password,
        "role": request.form['role']
    }}

    msg = user.create(dictn)
    flash(msg, 'success')
    return redirect(url_for('admin.add_user'))


@adminctrl.route('/delete')
def delete_user():
    if 'username' in session:
        admin = user.find_data(session['username'])
        if admin['role'].lower() != 'admin':
            flash("Permission denied!", "error")
            return redirect(url_for('admin.access_page'))
            exit()

        usrn = request.args.get('id')
        if session['username'] == usrn:
            flash("Permission denied", "error")
            return redirect(url_for('admin.user_page'))
            exit()

        del_user = user.delete_data(usrn)
        flash(del_user[1], del_user[0])
        return redirect(url_for('admin.user_page'))
    else:
        return redirect(url_for('login.login_GET'))


#Routing to the User upload page page for both GET and POST
@adminctrl.route('/manual')
def manual():
    if 'username' in session:
        the_user = user.find_data(session['username'])
        return render_template('admin/manual.html', user = the_user)
    else:
        return redirect(url_for('login.login_GET'))


#Routing for downloading .exe file
@adminctrl.route('/downloadffmpeg')
def download_ffmpeg():
    ffmpeg_download = Path(f'./storage/scripting/ffmpeg-git-full.7z')
    return send_file(ffmpeg_download, as_attachment=True)





    



