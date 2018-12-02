import socket
import threading
import argparse
import os
import os.path
import json
import mimetypes
from packet import Packet
from packet_constructor import Packet_Constructor
from packet_sender import Packet_Sender
from time import sleep


debug = False
file_dir = os.getcwd() + "/secure/"
p_constructor = Packet_Constructor()
handshake_completed = False

def startServer(host,port, dir):
    global file_dir
    file_dir = dir
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        conn.bind(('', port))
        print('File server is listening at', port)
        while True:
            data, sender = conn.recvfrom(1024)
            threading.Thread(target=packetHandler, args=(conn, data, sender)).start()
    finally:
        conn.close()


def get_file_mimetype(filename):
    if(os.path.isfile(file_dir + filename) == False):
        raise IOError("File " + filename + " does not exist.")  
    return mimetypes.guess_type(file_dir + filename)

def headers_fetch(data):
    headers = {}
    parsedData = data.split(CRLF)
    for i in range(1, len(parsedData)):
        header = parsedData[i]
        if header == '':
            break
        headerComponents = header.split(": ")
        headers[headerComponents[0]] = headerComponents[1]
    if(debug):
        print("The following headers were found")
        print(headers)
    return headers

def getHandler(parsedData):
    filename = get_filename(parsedData)
        
    if not filename:
        return str(os.listdir(file_dir)).encode('utf-8')
    else:
        if(os.path.isfile(file_dir + filename) == False):
            raise IOError("File " + filename + " does not exist for GET.")
        response_body = b''
        with open(file_dir + filename, 'rb') as file:
            while True:
                newData = file.read(1024)
                if not newData:
                    break
                response_body += newData
        return response_body
def clean_dirname(dname):
    dname = os.path.normcase(dname)
    return os.path.join(dname, '')

def in_cwd(fname):
    cwd = clean_dirname(os.getcwd())
    path = os.path.dirname(os.path.realpath(fname))
    path = clean_dirname(path)
    return path.startswith(cwd)

def postHandler(parsedData, header_data, body_data):
    post_command = parsedData[1]
    if(post_command == '/' or post_command == '\\'):
        raise SystemError("Command did not contain a file.")
    
    filename = post_command[1:]
    if(('~' in filename) or ('#' in filename) or ('%' in filename) or ('&' in filename) or ('*' in filename) or ('{' in filename) or ('}' in filename) or (':' in filename) or ('<' in filename) or ('>' in filename) or ('?' in filename) or ('+' in filename) or ('|' in filename) or ('"' in filename)):
        raise IOError("File " + filename + " is an invalid filename.")
    
    overwrite = True
    headers = headers_fetch(header_data)
    if headers and 'overwrite' in headers:
        overwrite = (headers['overwrite'] == 'true')
    if not overwrite:
        file_list = os.listdir(file_dir)
        if filename in file_list:
            if(os.path.isfile(filename) == True and overwrite == False):
                raise SystemError("File " + filename + " already exists for POST and overwrite was false.")
            return
    
    file = open(file_dir + filename, 'wb')

    if(body_data == CRLF.encode()):
        raise SystemError("Message body was empty.")
    file.write(body_data)

def packetHandler(conn,data,sender):
    global p_constructor
    global handshake_completed
    p = Packet.from_bytes(data)

    if(p.packet_type == Packet_Constructor.syn_type):
        if(debug):
            print("TCP syn received")        
        p.packet_type = Packet_Constructor.syn_ack_type
        conn.sendto(p.to_bytes(), sender)
    elif(p.packet_type == Packet_Constructor.ack_type):
        handshake_completed = True
        if(debug):
            print("TCP ack received")
    elif(handshake_completed):    
        payload = p_constructor.add_packet(p, conn, sender)    
        if(payload):
            print("Received last packet")
            response = dataHandler(payload, sender)
            print("Sending packets")
            print(response)
            sleep(0.1) # Time in seconds.
            Packet_Sender.send_as_packets(response, conn, sender, p.peer_ip_addr, p.peer_port)
            handshake_completed = False
        else:
            print("is not the last packet")

def dataHandler(data, addr):
    print(data)
    print(addr)
    print(data)
    print(addr)
    host = "localhost"
    crlf_count = 0
    header_data = b''
    body_data = b''
    for bit in data:
        bit = bit.to_bytes(1, byteorder='big')
        if crlf_count < 4:
            header_data += bit
            if (crlf_count == 0 or crlf_count == 2) and bit == b'\r':
                crlf_count += 1
            elif (crlf_count == 1 or crlf_count == 3) and bit == b'\n':
                crlf_count += 1
            else:
                crlf_count = 0
        else:
            body_data += bit
    header_data = header_data.decode('utf-8')
    parsedData = header_data.split()
    print("data")
    print(parsedData)
    response_body = ""
    try:
        response = "HTTP/1.1 200 OK%sConnection: keep-alive%sServer: %s%s"%(CRLF, CRLF, host, CRLF)
        if parsedData[0] == "GET":
            filename = get_filename(parsedData)
            checkIfGoodDirectoryGet(filename)
            if(debug):
                    print("GET request")
            if filename:
                if(debug):
                    print("GET request for file " + filename)
                type = get_file_mimetype(filename)
                filetype = type[0]
                if(filetype is None):
                    filetype = ""
                response = response + "Content-Disposition: attachment;filename=\"" + filename + "\"" + CRLF + "Content-Type: " + filetype + CRLF
            response_body = getHandler(parsedData)
        elif parsedData[0] == "POST":
            print("ok")
            filename = get_filename(parsedData)
            checkIfGoodDirectoryPost(filename)
            if(debug):
                print("POST request for file " + filename)
            response_body = postHandler(parsedData, header_data, body_data)
        bytes = response.encode('utf-8')
        if response_body:
            bytes = bytes + CRLF.encode('utf-8')
            bytes = bytes + response_body
            bytes = bytes + CRLF.encode('utf-8')
        return bytes

    except IOError as error:
        if(debug):
            print("404 File not found")
        response = "HTTP/1.1 404 ERROR: File could not be found%sConnection: keep-alive%sServer: %s%s"%(CRLF, CRLF, host, CRLF)
        response = response + str(error)
        bytes = response.encode('utf-8')
        return bytes

    except SystemError as error:
        if(debug):
            print("400 request invalid")
        response = "HTTP/1.1 400 ERROR: Bad Request%sConnection: keep-alive%sServer: %s%s"%(CRLF, CRLF, host, CRLF)
        response = response +str(error)
        bytes = response.encode('utf-8')
        return bytes
        #conn.sendall(bytes)
    except Exception as error:
        if(debug):
            print("401 non-authorized")
        response = "HTTP/1.1 403 ERROR: Security Error%sConnection: keep-alive%sServer: %s%s"%(CRLF, CRLF, host, CRLF)
        response = response + str(error)
        bytes = response.encode('utf-8')
        return bytes
        #conn.sendall(bytes)
