"""PyWeb a simple web server built in Python3."""
from socket import socket, AF_INET, SOCK_STREAM
import os
PORT = 80
IP = '0.0.0.0'
WEBSITE_FOLDER = 'website'
HOME_FILE = WEBSITE_FOLDER +  '/' + 'index.html'
ERROR_404_PAGE = '404.html'


#definging the serversocket variable and setting it to use the TCP protocol
SERVERSOCKET = socket(AF_INET, SOCK_STREAM)
SERVERSOCKET.bind((IP, PORT))
SERVERSOCKET.listen(10)

#welcome screen
print("Server started")
print("Port: " + str(PORT))


def load_binary(file):
    """Loading the target file and reading it as a binary."""
    with open(file, 'rb') as file2:
        return file2.read()


while True:
    (CLIENTSOCKET, ADDRESS) = SERVERSOCKET.accept()
    #getting browser stats
    DATA = bytes.decode(CLIENTSOCKET.recv(1024))

    #extract the file from the contence of the responce
    #try:
    PAGE = str(DATA).split()[1]
    #except:
        #pass

    print(WEBSITE_FOLDER + str(PAGE))

    #testing if the browser wants the root file
    if PAGE == '/':
        #tell the browser that the connection is good and what format to expect
        CLIENTSOCKET.send(str.encode("HTTP/1.1 200 OK\n"+"Content-Type: text/html\n"+"\n"))
        CLIENTSOCKET.send(load_binary(HOME_FILE))
    #testing if the browser asked for a css file
    elif PAGE.find('.css') != -1:
        CLIENTSOCKET.send(str.encode("HTTP/1.1 200 OK\n"+"Content-Type: text/css\n"+"\n"))
        CLIENTSOCKET.send(load_binary(WEBSITE_FOLDER + '/' + PAGE))
    else:
        #finding the file and sending it to the browser
        if os.path.isfile(WEBSITE_FOLDER + PAGE):
            #tell the browser that the connection is good and what format to expect
            CLIENTSOCKET.send(str.encode("HTTP/1.1 200 OK\n"+"Content-Type: text/html\n"+"\n"))
            CLIENTSOCKET.send(load_binary(WEBSITE_FOLDER + '/' +  PAGE))
        else:
            CLIENTSOCKET.send(str.encode("HTTP/1.1 200 OK\n"+"Content-Type: text/html\n"+"\n"))
            CLIENTSOCKET.send(load_binary(ERROR_404_PAGE))

    #closing the connection
    CLIENTSOCKET.close()
#closing the socket
SERVERSOCKET.close()
