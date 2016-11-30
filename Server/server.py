from listener import Listener

if __name__ == '__main__':
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 53))
	my_ip = s.getsockname()[0]
	my_port = 6000

	print("Starting Server " + my_ip + ":" + my_port)
	listener = Listener(my_ip, my_port)
	listener.start()