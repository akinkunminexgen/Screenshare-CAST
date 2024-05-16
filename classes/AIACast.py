# AIA Cast program - Created by:
# Akinkunmi Owolabi
# Idoreyin Ekanem
# André Barbosa Santos

import subprocess
import threading
from flask import Flask, request, jsonify
#========================3 - Start cast session=================================

# Class responsible for run CAST command 
class FFmpegCommandWithTimeLimit:
    def __init__(self, input_source="desktop"):
        self.input_source = input_source
        
        self.process = None
        self.stop_event = threading.Event()


    def gen_command_to_send(self, duration_minutes):
        """
        Generates the FFmpeg command with a time limit.
        """
        return (
            f"ffmpeg -f gdigrab -framerate 30 -i {self.input_source} "
            f"-t 00:{duration_minutes}:00 -vcodec libx264 -preset ultrafast "
            f"-tune zerolatency -f mpegts {self.output_url}"
        )
    
    


    def run_command(self, command_str, duration_minutes):
        """
        Executes the FFmpeg command with a timeout.
        """
        print(f"Running FFmpeg command: {command_str}")
        
        try:
            self.process = subprocess.Popen(command_str, shell=True)
            self.process.communicate(timeout=int(duration_minutes)*60)  # Wait for the duration or until the stop event is set
            self.process.kill()
        except TimeoutError as e:
            self.process.terminate()
            print(f"An error occurred: {e}")
            if self.process:
                self.process.kill()


    
    def exe_command_to_recieve(self, duration_minutes, output_url):

        self.command_to_recieve = f"ffplay -fflags nobuffer {output_url}"
        self.thread = threading.Thread(target=self.run_command,
                                   args=(self.command_to_recieve,
                                          duration_minutes))
        self.thread.start()
        return 'successful'
    

    
    def killer(self):
        kill_4_windows = f"taskkill /IM ffplay.exe /F"
        kill_4_linux = "sudo pkill -9 ffplay"        
        self.stop_event.set()  # Set the stop event to signal the thread to stop
        if self.process:
            subprocess.run(kill_4_windows, shell=True)
            self.process.kill()
    
    def killer_client(self):
        kill_4_windows = f"taskkill /IM exe2* /F"
        kill_4_linux = "sudo pkill -9 exe2"
        try:
            subprocess.run(kill_4_windows, shell=True)
        except FileNotFoundError as e:
            pass

# Example usage:
"""
input_source = "desktop"
output_url = "udp://10.0.1.103:1234"
ffmpeg_cmd = FFmpegCommandWithTimeLimit(
    input_source,
    output_url,
    duration_minutes)
ffmpeg_cmd.run_command()
"""


#==========================4 - Stop cast session================================
# To finish CAST Session manually, give the STOP CAST button the command:
#process.kill()