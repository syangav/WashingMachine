import socket

def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('google.com.hk', 0))
	print (s.getsockname()[0])
	return s.getsockname()[0]