from pathlib import Path
import json


class Jsonloader:

    #initializing path that leads to the supposed database
    
    message = ""
    msg = ""

    def __init__(self, name, path='data.json'):
        self.dbname = name.title()
        self.path = Path(f'./storage/{path}')
        self.message = ""

    #this method create attributes of various entities e.g USER QUESTION
    def create(self, jsonfile):
        #to read and load to json from the path initialized (data.json)
        file = self.path.read_text()
        file_data = json.loads(file)

        #looping through the attributes from user
        for key in jsonfile.keys():
            #check by confirming if the entity ID matches
            if key in file_data[self.dbname]:
                #display a message by concatenating the keys that exist
                self.message +=f"{key} already exists<br>"
                return self.message
            else:
                #once it does not match ensure to insert into the file
                file_data[self.dbname].update(jsonfile)
                self.path.write_text(json.dumps(file_data, indent=4))
                self.message = "Uploaded Successfully! <br>"
                return self.message
            break
            
                 
    #making a method to look for a piece of data
    def find_data(self, pointer):      
        file_data = json.loads(self.path.read_text())
        try:
            #return once it exists        
            return file_data[self.dbname][pointer]
        except KeyError:
            #return key errors if it discovers any key error
            return None


    #getting data from Json file to with number of data needed as parameter
    def get_data(self, num = 0):

        file_data = json.loads(self.path.read_text())

        try:
            if num == 0:
                return file_data[self.dbname]
            else:
                i = 1
                arr = {}
                #iteration to ensure it takes a chunk of data
                for keys, value in file_data[self.dbname].items():
                    arr[keys] = value
                    if i == num:
                        #this terminates the loop once the num passed has
                        #been reached
                        break
                    i+=1
                return arr#return the dictionary
        except KeyError:
            return None
    


    #update a particular set of data
    def update_data(self, pointer, **jsondata):

        file_data = json.loads(self.path.read_text())

        try:
            #confirming if a set of data exists
            if self.find_data(pointer) != 'Null':
                for key, value in file_data[self.dbname][pointer].items():
                    
                    for k2, v2 in jsondata.items():
                        #checking if the two(db-info & new-info) keys match
                        if key == k2:
                            file_data[self.dbname][pointer][key] = v2

                self.path.write_text(json.dumps(file_data, indent=4))
            return 'Updated successfully!'
        except KeyError:
            return 'An error has occurred due to wrong keys!'            

    #delete a particular set of data
    def delete_data(self, pointer):

        file_data = json.loads(self.path.read_text())

        try:
            if self.find_data(pointer) != 'Null':
                #this pop out the data passed for deletion
                file_data[self.dbname].pop(pointer)

            self.path.write_text(json.dumps(file_data, indent=4))
            return ['success', 'Deleted successfully!']
        except KeyError:
            return ['error', 'Cannot be found!']
        

        



        
    