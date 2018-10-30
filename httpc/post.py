import socket
import json
from urlParsing import parseURL, parseReponse

def postUrl(verbose,url,headers, data, parsed_file_data):
    urlParsed = parseURL(url, None)
    s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    print(urlParsed['host'])
    s.connect((urlParsed['host'], 80))
    if parsed_file_data:
        fileData = ""
        for c in parsed_file_data['fields']:
            fileData += c
        s.send(b'POST '+urlParsed['destination']+ ' HTTP/1.0\r\nHost: ' + urlParsed['host']+'\r\nContent-Type:' + parsed_file_data['boundary']+'\r\nContent-Length:1024'+'\r\n\r\n'+fileData)
    s.send(b'POST '+urlParsed['destination']+ ' HTTP/1.0\r\nHost: ' + urlParsed['host']+'\r\nContent-Type:' + headers['Content-Type']+'\r\nContent-Length:'+str(len(str(data)))+'\r\n\r\n'+json.dumps(data))
    response = s.recv(4096)
    parseReponse(None,response,verbose)
    s.close()


