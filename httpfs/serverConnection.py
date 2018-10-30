import socket
import sys
from thread import *
import cmdServerValues
import os


def startServer(HOST,PORT, dir):
    client = {}
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')
        
    #Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
            
    print('Socket bind complete')
        
    #Start listening on socket
    s.listen(10)
    print('Socket now listening')
        
    #Function for handling connections. This will be used to create threads
    def clientthread(conn):
        #Sending message to connected client
        conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
            
        #infinite loop so that function do not terminate and thread do not end.
        while True:
          #Receiving from client
            data = conn.recv(1024)
            os.chdir(dir)
            clientValues = cmdServerValues.parse_data(data, dir)
            if '404' in clientValues:
                reply = 'Bad Request. Closing connection now. Bye \n'
                conn.sendall(reply)
                conn.close()
                print("closed connection for " + client[conn][0]+':'+str(client[conn][1]))
                break
            elif "401" in clientValues:
                reply = 'No authorization \n'
                conn.sendall(reply)
                conn.close()
                print("closed connection for " + client[conn][0]+':'+str(client[conn][1]))


            reply = clientValues + '\n'
            if not data: 
                break
                
            conn.sendall(reply) 
        #came out of loop
        #conn.close() 
    while True:
        try:
            #wait to accept a connection - blocking call
            conn, addr = s.accept()
            client[conn] = addr
            print('Connected with ' + addr[0] + ':' + str(addr[1]))

            #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            start_new_thread(clientthread ,(conn,))
        except KeyboardInterrupt:
            exit()
    s.close()

