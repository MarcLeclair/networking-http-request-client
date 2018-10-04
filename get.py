import socket
import json


def getUrl(verbose, url)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("cnn.com", 80))
    s.send(request)
    response = s.recv(4096, socket.MSG_WAITALL)

    if verbose == True:
        data = response.decode("utf-8")
        (headers, js) = data.split("\r\n\r\n")
        jsonValues = json.loads(js)
        print(json.dumps(jsonValues, indent=4))
    else:
        while (len(result) > 0):
            data = result.decode("utf-8")
            print(data)
            result = s.recv(4096)