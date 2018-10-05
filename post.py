import socket
import json
def postUrl(verbose,url,headers, data):
    urlParsed = parseURL(url)

    s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    print(urlParsed)
    s.connect((urlParsed['host'], 80))

    s.send(b'POST '+urlParsed['destination']+ ' HTTP/1.0\r\nHost: ' + urlParsed['host']+'\r\nContent-Type:' + headers['Content-Type']+'\r\nContent-Length:'+str(len(str(data)))+'\r\n\r\n'+json.dumps(data))
    response = s.recv(4096)
    parseReponse(response,verbose)
    s.close()

def parseURL(url):
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

