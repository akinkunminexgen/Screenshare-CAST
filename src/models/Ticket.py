from classes.Jsonloader import *
from pathlib import Path
from flask import Flask

#class User inheriting the class Jsonloader
class Ticket(Jsonloader):

    #Adding an attribute called privileges that gives users role
    def __init__(self, name='ticket'):
        """Initialize attributes of the parent class."""
        Jsonloader.__init__(self, name)

    def fmt(self, data, timer):
        Dat = {data :
               {"timer" : timer}
               }
        return Dat



    

            