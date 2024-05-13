# AIA Cast program - Created by:
# Akinkunmi Owolabi
# Idoreyin Ekanem
# André Barbosa Santos

import subprocess
import os, time
import requests
import shutil


def install_ffmpeg():
    
    # URL of the file to download
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z"
    # Path to save the downloaded file
    download_path = "ffmpeg-git-full.7z"
    # Path to 7z.exe (adjust this path based on your 7-Zip installation)
    seven_zip_path = "C:\\Program Files\\7-Zip\\7z.exe"
    # Path to save the decompressed folder
    decompressed_folder_path = os.path.expanduser("~\\Documents\\ffmpeg")
    # Path to the existing ffmpeg folder
    existing_ffmpeg_path = os.path.join(decompressed_folder_path, 'ffmpeg')

    #check to know if ffmpeg exists
    if os.path.exists(existing_ffmpeg_path):
        pass
    else:
        #shutil.rmtree(existing_ffmpeg_path)
        # Download the file
        response = requests.get(url)
        with open(download_path, 'wb') as file:
            file.write(response.content)

        # Decompress the .7z file using 7z.exe
        extract_cmd = f'"{seven_zip_path}" x -y {download_path} -o{decompressed_folder_path}'
        subprocess.run(extract_cmd, shell=True)

        

        # Find the 'bin' folder within the decompressed folder
        for root, dirs, files in os.walk(decompressed_folder_path):
            if 'bin' in dirs:
                bin_folder_path = os.path.join(root, 'bin')
                break

        # Create a new path based on the 'bin' folder location
        new_path = os.path.join(bin_folder_path)

        # Add the new path to the PATH environment variable for the current session
        os.system(f'setx PATH "%PATH%;{new_path}"')

        # Print the new path created based on the 'bin' folder location
        print("Custom path created based on the location of the 'bin' folder:")
        print(new_path)

        print("Download and extraction completed successfully. Please restart your CMD for changes to take effect.")




def run_ffmpeg(timer, udpip):   
    print(udpip)
    # Define the ffmpeg command
    tim = ""
    if int(timer) < 10:
        tim = f"0{timer}"
    else:
        tim = timer

    command = f"ffmpeg -f gdigrab -framerate 60 -i desktop -t 00:{tim}:00 -c:v libx264 -preset ultrafast -tune zerolatency -f mpegts {udpip}"
    print(command)
    try:
        # Run the ffmpeg command
        process = subprocess.Popen(command, shell=True)
        process.communicate(timeout=int(timer)*60)
        process.kill()
        #process = subprocess.run(command, shell=True)
        print("ffmpeg command executed successfully.")
        print('generating')
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        process.kill()
if __name__ == "__main__":
    install_ffmpeg()
    run_ffmpeg("5", "udp://10.0.0.174:9944")
