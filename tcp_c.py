import socket

target_host = 'www.google.pl'
target_port = 80

#creating socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connecting to client
client.connect((target_host,target_port))

#sending data
client.send('GET / HTTP/1.1\r\nHost: google.pl\r\n\r\n')

response = client.recv(4096)

print response
