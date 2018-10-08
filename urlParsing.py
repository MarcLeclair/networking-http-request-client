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