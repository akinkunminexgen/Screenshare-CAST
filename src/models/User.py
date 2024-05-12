from classes.Jsonloader import *
from pathlib import Path
from flask import Flask
from flask_bcrypt import Bcrypt

#class User inheriting the class Jsonloader
class User(Jsonloader):

    #Adding an attribute called privileges that gives users role
    def __init__(self, name='user'):
        """Initialize attributes of the parent class."""
        Jsonloader.__init__(self, name)



    def load_txt_file(self, data):
        app = Flask(__name__)
        bcrypt = Bcrypt(app)

        dictn = {}
        dict_format = {}

        for info in data.splitlines():#looping to get all lines
            #some keywords must be considered while importing a file
            if 'age' in info:
                new_data = info.split(':')
                x = {"age" : new_data[-1].strip()}
                dictn.update(x)
            
            elif 'occupation' in info:
                new_data = info.split(':')
                x = {"designation" : new_data[-1].strip()}
                dictn.update(x)

            elif ' name' in info:
                new_data = info.split(':')
                name = new_data[-1].strip().split()
                #get the firstname and lastname by splitting the string
                x = {"Firstname" : name[0], 
                     "Lastname" : name[1]}
                dictn.update(x)

            elif 'gender' in info:
                new_data = info.split(':')
                x = {"gender" : new_data[-1].strip()}
                dictn.update(x)

            elif 'password' in info:
                new_data = info.split(':')
                #hashing the password into a cipher text
                pw_hash = bcrypt.generate_password_hash(
                        new_data[-1].strip()).decode('utf-8')
                x = {"password" : pw_hash}
                dictn.update(x)

            elif 'student' in info:
                new_data = info.split(':')
                x = {"role" : "Student"}
                if new_data[-1].strip().lower() == 'no':
                    x = {"role" : "Admin"}
                dictn.update(x)
            
            elif 'username' in info:
                new_data = info.split(':')
                the_id = new_data[-1].strip()
            else:
                pass

        #update the file with new set of dictionary
        the_format = {the_id : dictn}
        dict_format.update(the_format)

        return self.create(dict_format)

            