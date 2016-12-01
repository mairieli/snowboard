import socket
from listener import Listener

if __name__ == '__main__':
    # Get IP and Server Port 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 53))
        my_ip = s.getsockname()[0]
    except Exception as e:
        print("MY IP: ", end="")
        my_ip = input()
    my_port = 6000

    print("Starting Server " + my_ip + ":" + str(my_port))
    listener = Listener(my_ip, my_port)
    listener.start()