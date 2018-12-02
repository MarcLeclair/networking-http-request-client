from redirect import redirectedUrl

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
    
    if hostString.startswith("http://") or hostString.startswith("https://"):
        hostString = hostString[7:]
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


def parseReponse(url,pieces,verbose):
    flag = False
    iterator = iter(pieces.split("\n"))
    headers = ""
    for line in iterator:
        headers += line+"\n"
        if "300" in line or "301" in line or "302" in line:
            flag = True
        if not line.strip():  # empty line
            break
    
    body = "\n".join(iterator)
    
    if flag:
        redirectedUrl(url,verbose, headers, "")
    else:
        if verbose:
            print(headers)
            print(body)
        else:
            print(body)

def parse_packet_response(response):
    status = ""
    code = ""
    body = ""
    header = ""
    value = 0
    crlf_count = 0

    header_data = b''
    body_data = b''
    for bit in response:
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

    for c in range(len(header_data)):
        if header_data[c] == "HTTP/1.1":
            code = header_data[c + 1]
            status = header_data[c + 2]
    
    for c in range(len(header_data)):
        if header_data[c] != "chunked":
            header += header_data[c]
            header += " "
        if header_data[c] == "chunked":
            header += header_data[c]
            header += " "
            value = c + 1
            break
    for c in range(len(header_data)):
        if c < value:
            continue
        else:
            body += header_data[c]
            body += " "
        
    display = {"status": status, "code": code, "body": body, "header": header, "response": response}
    return display