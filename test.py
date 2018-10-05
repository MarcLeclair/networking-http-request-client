import socket
import json

url = "http://www.httpbin.org/status/418"
hostString = ""
destination = ""
indexFirstDot =0
counter = 0
for i in range(0, len(url)):
    if url[i] == '.' and counter == 0:
        counter += 1
        indexFirstDot = i
    elif url[i]  == '.' and counter == 1:
        counter += 1
    elif url[i] == '/' and counter >=2:
        hostString = url[indexFirstDot+1 : i]
        destination = url[i:]
        break

print hostString
print destination