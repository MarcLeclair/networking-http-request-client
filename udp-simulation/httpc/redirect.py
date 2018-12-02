from httpsredirection import getSecuredConnection

#handles redirect with the location fields from the response
#However, some reponse gives back an HTTPS response and will therefore be redirected to the httpsredirection file for SSL connection
def redirectedUrl(url, verbose, headers, keyValues):
    iterator = iter(headers.split("\n"))
    joinedHeader = ""
    redirectedUrl = ""
    for line in iterator:
        joinedHeader += line+"\n"
        if "Location" in line:
           redirectedUrl = line.split(':',1)[1].strip()
    rediretedLocation = ""
    
    if  redirectedUrl.startswith("https://"):
        getSecuredConnection(redirectedUrl[8:-1])
    
    else:
        if redirectedUrl.startswith("http://"):
            rediretedLocation = redirectedUrl
        else:
            rediretedLocation = url+redirectedUrl
        print(rediretedLocation)
        get.getUrl(verbose, rediretedLocation, "")


import get