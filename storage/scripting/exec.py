# AIA Cast program - Created by:
# Akinkunmi Owolabi
# Idoreyin Ekanem
# André Barbosa Santos

import subprocess
import os, time
import requests
import shutil
from pathlib import Path




def install_ffmpeg(ip):
    
    print("Without 7zip the application will stop, you need to install it")
    print("if this application stops, ensure to restart it")
    print("you can exit this application by closing it on the top right corner")
    print("\nstarting...")
    time.sleep(4)


    # URL of the file to download
    #url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z"
    url = f"http://{ip}/admin/downloadffmpeg"
    # Path to save the downloaded file
    download_path = os.path.expanduser("~\\Downloads\\ffmpeg-git-full.7z")
    # Path to 7z.exe (adjust this path based on your 7-Zip installation)
    seven_zip_path = "C:\\Program Files\\7-Zip\\7z.exe"
    # Path to save the decompressed folder
    decompressed_folder_path = os.path.expanduser("~\\Documents\\ffmpeg")
    # Path to the existing ffmpeg folder
    #existing_ffmpeg_path = os.path.join(decompressed_folder_path, 'ffmpeg')
    print(url)

    #check to know if ffmpeg exists
    if os.path.exists(decompressed_folder_path):
        print(f"ffmpeg already exists at {decompressed_folder_path}")
        time.sleep(1)
    else:
        try:
            # Download the file
            response = requests.get(url)
            response.raise_for_status()
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

        except requests.RequestException as e:
            print(f"Download failed: {e}")
            time.sleep(1)
        except subprocess.CalledProcessError as e:
            print(f"Extraction failed: {e}")
            time.sleep(1)



def run_ffmpeg(timer, udpip):   
    print(udpip)
    # Define the ffmpeg command
    tim = ""
    if int(timer) < 10:
        tim = f"0{timer}"
    else:
        tim = timer

    command = f"ffmpeg -f gdigrab -framerate 30 -i desktop -t 00:{tim}:00 -c:v libx264 -preset ultrafast -tune zerolatency -f mpegts {udpip}"
    print(command)
    try:
        print('generating')
        # Run the ffmpeg command
        process = subprocess.Popen(command, shell=True)
        process.communicate(timeout=int(timer)*60)
        process.kill()
        #process = subprocess.run(command, shell=True)
        print("ffmpeg command executed successfully.")
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        process.kill()

if __name__ == "__main__":
    install_ffmpeg("the_ip")
    run_ffmpeg("the_timer", "the_udpip")
