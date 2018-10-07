def redirectedUrl(url, verbose, headers, keyValues):
    iterator = iter(headers.split("\n"))
    joinedHeader = ""
    redirectedUrl = ""
    for line in iterator:
        joinedHeader += line+"\n"
        if "Location" in line:
           redirectedUrl = line.split(':',1)[1].strip()
    get.getUrl(verbose, url+redirectedUrl, "")


import get