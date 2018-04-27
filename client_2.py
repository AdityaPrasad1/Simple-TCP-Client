#! /lusr/bin/python

# ap45485
# CS 356 - Lam
# Exercise 1

import socket
import random

# Server socket informatoin
server_ip = '128.83.144.56'
server_port = 35603

# Create psock, bind to available port, listen
psock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
psock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
psock.bind((socket.gethostname(), 35602))
bind_ip, bind_port = psock.getsockname()
print '\n-------------------------------------------'
print 'psock Address: ' + bind_ip + '\n'
print 'psock Port: ' + str(bind_port) + '\n'
psock.listen(1)

# Create client socket, get information
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Client request string information, connect to server and send
request_type = 'ex1'
connection_specifier = server_ip + '-' + str(server_port) + ' ' + bind_ip + '-' + str(bind_port)
usernum = random.randint(0, 9000)
username = 'A.S.Prasad'
request = request_type + ' ' + connection_specifier + ' ' + str(usernum) + ' ' + username + '\n'
sock.connect((server_ip, server_port))
client_ip, client_port = sock.getsockname()
sock.send(request)

# Server confirmation information, receive until second newline
confirmation = ''
c_count = 0
while c_count != 2:
    data = sock.recv(1)
    confirmation = confirmation + data
    if data == '\n':
        c_count += 1
print 'Server Confirmation: \n' + confirmation
tokens = confirmation.split('\n')
conf_tokens = tokens[1].split(' ')

# Check if server responds with OK, otherwise print error
if conf_tokens[0] != 'OK':
    sock.close()
    print 'ERROR: ' + ' '.join(conf_tokens)
    quit()
id_num = conf_tokens[1]
servernum = int(conf_tokens[3])
print 'Server Number 1: ' + str(servernum) + '\n'

# Accept on psock, and receive on new socket
newsock, addr = psock.accept()
confirmation2 = ''
c_count = 0
while c_count != 1:
    data = newsock.recv(1)
    confirmation2 = confirmation2 + data
    if data == '\n':
        c_count += 1
conf2_tokens = confirmation2.split('\n')
conf2_tokens = conf2_tokens[0].split(' ')
newservernum = int(conf2_tokens[4])
print 'Server Number 2: ' + str(newservernum) + '\n'
print 'CS 356 server calling ' + str(newservernum) + '\n'

# Client ack, send to server through new socket then close
client_ack = str(servernum + 1) + ' ' + str(newservernum + 1) + '\n'
newsock.send(client_ack)
newsock.close()

# Receive server ack until first newline, then close socket
server_ack = ''
s_count = 0
while s_count != 1:
    data = sock.recv(1)
    server_ack = server_ack + data
    if data == '\n':
        s_count += 1;
print 'Server Ack: ' + server_ack
sock.close()

# Verify if server ack is OK, otherwise print error
s_tokens = server_ack.split('\n')
s_tokens = s_tokens[0].split('\t')
if s_tokens[0] != 'OK':
    print 'ERROR: ' + server_ack
    quit()
fservernum = s_tokens[1]
print 'Server Number 3: ' + str(fservernum)
print '-------------------------------------------\n'

# Close connection
psock.close()
