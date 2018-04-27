#! /lusr/bin/python

# ap45485
# CS 356 - Lam
# Exercise 0

import socket
import random

# Server socket informatoin
server_ip = '128.83.144.56'
server_port = 35603

# Create client socket and connect to server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect((server_ip, server_port))

# Client socket information
client_ip, client_port = sock.getsockname()

# Client request string information
request_type = 'ex0'
connection_specifier = server_ip + '-' + str(server_port) + ' ' + client_ip + '-' + str(client_port)
usernum = random.randint(0, 9000)
username = 'A.S.Prasad'
request = request_type + ' ' + connection_specifier + ' ' + str(usernum) + ' ' + username + '\n'
sock.send(request)

# Server confirmation information, receive until second newline
confirmation = ''
c_count = 0
while c_count != 2:
    data = sock.recv(1)
    confirmation = confirmation + data
    if data == '\n':
        c_count += 1
print '\n-------------------------------------------'
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

# Client ack, send to server
client_ack = request_type + ' ' + str(usernum + 1) + ' ' + str(servernum + 1) + '\n'
sock.send(client_ack)

# Receive server ack until first newline
server_ack = ''
s_count = 0
while s_count != 1:
    data = sock.recv(1)
    server_ack = server_ack + data
    if data == '\n':
        s_count += 1
print 'Server Ack: ' + server_ack

# Verify if server ack is OK, otherwise print error
s_tokens = server_ack.split(' ')
if s_tokens[0] != 'CS':
    sock.close()
    print 'ERROR: ' + server_ack
    quit()
if s_tokens[9] != 'OK':
    sock.close()
    print 'ERROR: ' + server_ack
    quit()
print 'Server Number 2: ' + str(s_tokens[10]) + '-------------------------------------------\n'

# Close connection
sock.close()
