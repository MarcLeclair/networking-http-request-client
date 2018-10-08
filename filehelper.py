#Logic taken from requests github implementation for educational purposes
from collections import Mapping
from io import BytesIO
import os
import binascii
import codecs

#class req to keep track of the files content , headers, name and extension
class Req:
    name= ''
    filename = ''
    data = None
    headers = None

#this file will iterate through a file and get its value with the boundary needed to send a POST request
writer = codecs.lookup('utf-8')[3]
try:
    basestring
except NameError:
    basestring = str

def choose_boundary():
    boundary = binascii.hexlify(os.urandom(16))
    return boundary

def encode_multipart_formdata(fields, boundary=None):
    body = BytesIO()
    if boundary is None:
        boundary = choose_boundary()
    for field in fields:
        body.write(b'--%s\r\n' % (boundary))
        data = field
        if isinstance(data, int):  
            body.write("Content-Disposition: form-data; name=\"one\"; filename=\"newfile.txt\"")
            data = str(data)  # Backwards compatibility
        if isinstance(data, str):
            body.write("Content-Disposition: form-data; name=\"one\"; filename=\"newfile.txt\"\r\n")
            writer(body).write(data)
        else:
            if data is None:
                body.write("")
            else:
                print("data is" + data)
                body.write(data)
        body.write(b'\r\n')
    content_type = str('multipart/form-data; boundary=%s' % boundary)
    return body.getvalue(), content_type


def guess_filename(obj):
    """Tries to guess the filename of the given object."""
    name = getattr(obj, 'name', None)
    if (name and isinstance(name, basestring) and name[0] != '<' and
            name[-1] != '>'):
        return os.path.basename(name)

def multipart(self, content_disposition=None, content_type=None,
                       content_location=None):
        headers = {'Content-Disposition' : ""}
        self.headers['Content-Disposition'] = 'form-data'
        self.headers['Content-Disposition'] += '; '.join([
            '', self._render_parts(
                (('name', self._name), ('filename', self._filename))
            )
        ])
        self.headers['Content-Type'] = content_type
        self.headers['Content-Location'] = content_location

def getContent(filePath):
    value = {'txt': open(filePath,'rb')}

    if value is None:
        a = 2
    if isinstance(value, (str, bytes, bool, int)):
        raise ValueError('cannot encode objects that are not 2-tuples')
    if isinstance(value, Mapping):
        value = value.items()
    new_fields=[]
    for (k, v) in value:
        # support for explicit filename
        ft = None
        fh = None
        if isinstance(v, (tuple, list)):
            if len(v) == 2:
                fn, fp = v
            elif len(v) == 3:
                fn, fp, ft = v
            else:
                fn, fp, ft, fh = v
        else:
            fn = guess_filename(v) or k
            fp = v

        if isinstance(fp, (str, bytes, bytearray)):
            fdata = fp
        elif hasattr(fp, 'read'):
            fdata = fp.read()
        elif fp is None:
            continue
        else:
            fdata = fp
        req = Req()
        req.name = k
        req.data = fdata
        req.filename = fn
        req.headers = fh
        new_fields.append(k)
        new_fields.append(fdata)
        new_fields.append(fn)
        new_fields.append(fh)
        new_fields = encode_multipart_formdata(new_fields)
        boundary = new_fields[len(new_fields)-1]

        print(boundary)
        return {'fields': new_fields[:-1], 'Content-Type': boundary}


