import socket

class NetworkUtils:
    @staticmethod
    def get_local_ip():
        try:
            # Create a socket object
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # Connect to any remote server
            s.connect(("8.8.8.8", 80))
            
            # Get the local IP address from the socket's address
            local_ip = s.getsockname()[0]
            
            # Close the socket
            s.close()
            
            return local_ip
        except socket.error as e:
            print("Error:", e)
            return None
