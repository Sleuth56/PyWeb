#!/usr/bin/python3

#------PyWeb a simple web server built in Python3------
from socket import socket, AF_INET, SOCK_STREAM
import os

PORT = 80
IP = '0.0.0.0'
WEBSITE_FOLDER = 'website'
HOME_FILE = WEBSITE_FOLDER +  '/' + 'index.html'
ERROR_404_PAGE = '404.html'


#------starting TCP socket server------
SERVERSOCKET = socket(AF_INET, SOCK_STREAM)
SERVERSOCKET.bind((IP, PORT))
SERVERSOCKET.listen(10)

#------welcome screen------
print("Server started")
print("Port: " + str(PORT))


#------Loads the target file and reading it in as bytes------
def load_file(file):
    with open(file, 'rb') as file2:
        return file2.read()


while True:
    (CLIENTSOCKET, ADDRESS) = SERVERSOCKET.accept()
    #------Gets browser stats------
    DATA = bytes.decode(CLIENTSOCKET.recv(1024))

    #------extracts the file from the contence of the responce------
    PAGE = str(DATA).split()[1]

    print(WEBSITE_FOLDER + str(PAGE))

    #------if the browser wants the root file------
    if PAGE == '/':
        #------send OK and the root html file------
        CLIENTSOCKET.send(str.encode("HTTP/1.1 200 OK\n"+"Content-Type: text/html\n\n"))
        CLIENTSOCKET.send(load_file(HOME_FILE))
    #------if the browser asked for a css file------
    elif PAGE.find('.css') != -1:
        CLIENTSOCKET.send(str.encode("HTTP/1.1 200 OK\n"+"Content-Type: text/css\n\n"))
        CLIENTSOCKET.send(load_file(WEBSITE_FOLDER + '/' + PAGE))
    #------send OK and the html file the browser asked for------
    else:
        if os.path.isfile(WEBSITE_FOLDER + PAGE):
            CLIENTSOCKET.send(str.encode("HTTP/1.1 200 OK\n"+"Content-Type: text/html\n\n"))
            CLIENTSOCKET.send(load_file(WEBSITE_FOLDER + '/' +  PAGE))
        #------send the ERROR_404_PAGE------
        else:
            CLIENTSOCKET.send(str.encode("HTTP/1.1 200 OK\n"+"Content-Type: text/html\n\n"))
            CLIENTSOCKET.send(load_file(ERROR_404_PAGE))

    #------close the connection------
    CLIENTSOCKET.close()
#------close the socket------
SERVERSOCKET.close()
