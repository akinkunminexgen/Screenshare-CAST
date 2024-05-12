from pathlib import Path
import shutil
import os

class TransformToExe:

    #initializing path that leads to the supposed files

    def __init__(self):
        self.parent_dir = os.path.dirname(os.path.dirname
                                          (os.path.abspath(__file__)))
        self.source_path = Path(f'./storage/scripting/exec.py')
        self.destination_path = Path(f'./storage/scripting/exec2.py')
        self.message = None

    def copy_file(self):
        try:
            #always empty file
            self.destination_path.write_text('')
            filing = self.destination_path.read_text()
            if filing == "":                
                shutil.copyfile(self.source_path, self.destination_path)
            self.message = "successful"
        except Exception as e:
            self.message = "An error has occured!"
        
        return self.message
    
    def alter_file(self, timer, udpip):
        filing = self.destination_path.read_text()
        Data = filing.splitlines()
        i = 0
        for data in Data:#looping to get all lines
            
            if 'the_timer' in data:
                newline = data.replace('the_timer', timer)
                newline = newline.replace("the_udpip", udpip)
        
                print(newline, i)
                Data[int(i)] = newline
            i+= 1
        
        self.destination_path.write_text('\n'.join(Data) + '\n')


