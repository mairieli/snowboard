from listener import Listener

if __name__ == '__main__':
	print("Starting Server...")
	listener = Listener('', 6000)
	listener.start()