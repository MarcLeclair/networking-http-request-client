import socket
import json

def getUrl(verbose, url, keyValues):
    urlParsed = parseURL(url,keyValues)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((urlParsed['host'], 80))
    print(urlParsed)
    s.send("GET "+urlParsed['destination']+" HTTP/1.1\r\nHost: "+urlParsed['host']+"\r\n\r\n")
    response = s.recv(4096)
    if len(response) < 4096:
        parseReponse(response,verbose)
    else:
        while (len(response) > 0):
            data = response.decode("utf-8")
            response = s.recv(4096)
        parseReponse(data,verbose)
    s.close()
    
def parseURL(url,keyValues):
    hostString = ""
    destination = ""
    counter = 0
    for i in range(0, len(url)):
        if url[i]  == '.' and counter == 0:
            counter += 1
        elif url[i] == '/' and counter ==1:
            hostString = url[:i]
            destination = url[i:]
            break
    if destination == "":
        raise Exception("Your link is incomplete, you are missing the request with the link (i.e: /status/418)")
    if keyValues:
        aggregatedValues = ""
        for key, value in keyValues.items():
            if aggregatedValues == "":
                aggrhttpegatedValues += key+"="+value
            else:
                aggregatedValues +="&"+key+"="+value
        destination+"?"+aggregatedValues
    return {'host': hostString, 'destination':destination}

def parseReponse(pieces,verbose):
    iterator = iter(pieces.split("\n"))
    headers = ""
    for line in iterator:
        headers += line+"\n"
        if not line.strip():  # empty line
            break

    body = "\n".join(iterator)
    if verbose:
        print(headers)
        print(body)
    else:
        print(body)