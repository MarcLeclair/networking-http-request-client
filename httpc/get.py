import socket
import json
from redirect import redirectedUrl
from urlParsing import parseReponse, parseURL

def getUrl(verbose, url, keyValues):
    urlParsed = parseURL(url,keyValues)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((urlParsed['host'], 80))
    s.send("GET "+urlParsed['destination']+" HTTP/1.0\r\nHost: "+urlParsed['host']+"\r\n\r\n")
    response = s.recv(4096)
    if len(response) < 4096:
        parseReponse(urlParsed['host'],response,verbose)
    else:
        while (len(response) > 0):
            data = response.decode("utf-8")
            response = s.recv(4096)
        parseReponse(urlParsed['host'],data,verbose)
    s.close()
    