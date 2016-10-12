import socket

target_host = 'www.google.pl'
target_port = 80

#utworzenie obiektu gniazda
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#polaczenie sie z klientem
client.connect((target_host,target_port))

#wysylanie danych
client.send('GET / HTTP/1.1\r\nHost: google.pl\r\n\r\n')

response = client.recv(4096)

print response
