import sys
import argparse
import os
import json
import fileParser

sys.dont_write_bytecode = True

def parse_data(data, cur_dir):
    try:
        result = data.decode('utf-8')
        if 'GET' in result:
            parsedData = result.split(" ")

            for string in parsedData:
                if '/' in string:
                    file_list = os.listdir(cur_dir)
                    fileName = string.split('/')[1]
                    fileName = fileName.strip('\n')
                    fileName = fileName.strip('\r')
                    if '.' in fileName:
                        if in_cwd(fileName) is False:
                            return "401"
                        if fileName in file_list:
                            return fileParser.parse_file(fileName)
                        else:
                            return "No such files exist. Or maybe it was a typo. Who knows"       
                    else:
                        return str(file_list)
                   
            return "404"
        elif 'POST' in result:
            parsedData = result.split(" ", 2)
            fileName = ""
            dataToWrite = parsedData[-1]
            if '/' in dataToWrite:
                dataToWrite = " "
            for string in parsedData:
                if '/' in string:
                    fileName = string.split('/')[1]
                    fileName = fileName.strip('\n')
                    fileName = fileName.strip('\r')
                    file_list = os.listdir(cur_dir)
                    if fileName in file_list:
                        fileParser.overwrite_file(fileName, dataToWrite)
                    else:
                        fileParser.create_new_file(fileName,dataToWrite)
                    return "file overwritten"
        else:
            return "404"
    except UnicodeDecodeError:
        return "Unicode decoded error"

def clean_dirname(dname):
    dname = os.path.normcase(dname)
    return os.path.join(dname, '')

def in_cwd(fname):
    cwd = clean_dirname(os.getcwd())
    path = os.path.dirname(os.path.realpath(fname))
    path = clean_dirname(path)
    return path.startswith(cwd)
