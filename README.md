# Screenshare-CAST
With the use of FFMPEG to share screen from two devices 


## Installation
To install Screenshare-CAST and its dependencies, use pip:

```bash
pip install flask
pip install flask-bcrypt
pip install shutils
pip install pyinstaller

```
## Usage
The two devices has to be on the same network

Streaming session can be initiated by the administrator (with ticket and timer) using FFMPEG conmand through the system terminal

7zip has to be installed before executing the .exe file

.executable file will be generated so as to send frames through UDP protocol to the server



## Limitation
.exe does not work on linux hence dynamic screen share can not be achieved

