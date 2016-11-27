from listen import Listen

if __name__ == '__main__':
	print("Starting Server...")
	listen = Listen('', 5000)
	listen.start()