import socket, ssl

def getSecuredConnection(url):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(url)
    s.connect((url, 443))
    s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
    s.sendall("GET / HTTP/1.1\r\nHost:"+url+"\r\nConnection: close\r\n\r\n")

    while True:
        new = s.recv(4096)
        if not new:
            s.close()
            break
        print new
    