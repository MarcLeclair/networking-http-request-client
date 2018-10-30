import csv
import json

def parse_file(fileName):
    fileEnding = fileName.split(".")[1]
    if "csv" in fileEnding:
        file=open( fileName, "r")
        reader = csv.reader(file)
        text = "---------- Beginning of CSV file --------------\n"
        for line in reader:
            text += str(line) + "\n"
        text += "\n--------- End of CSV file --------------------"
        return text
    elif "txt" in fileEnding:
        f = open(fileName,'r')
        text = "---------- Beginning of TEXT file --------------\n"
        for line in f:
            text += line
        text += "\n--------- End of TEXT file --------------------"
        f.close()
        return text
    elif "json" in fileEnding:
        with open(fileName) as f:
            data = json.load(f)
        return json.dumps(data)

def overwrite_file(fileName, data):
    f = open(fileName, 'r+')
    text = f.read()
    text = data
    f.seek(0)
    f.write(text)
    f.truncate()
    f.close()

def create_new_file(fileName, data):
    f= open(fileName,"w+")
    f.write(data)
    f.close()


