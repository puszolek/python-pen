import socket
import threading

bind_ip = '0.0.0.0'
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip, bind_port))

server.listen(5)

print 'Listening on port {}:{}'.format(bind_ip, bind_port)

#thread to handle client
def handle_client(client_socket):

	#print info from the client
	request = client_socket.recv(1024)
	print 'Received {}'.format(request)

	#sending back
	client_socket.send('hello!')
	client_socket.close()


while True:
	client, addr = server.accept()

	print 'Connected to {}:{}'.format(addr[0], addr[1])

	#create client thread to handle incoming data
	cilent_handler = threading.Thread(target=handle_client, args=(client,))
	client_handler.start()
