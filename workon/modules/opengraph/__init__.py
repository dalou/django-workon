# encoding: utf-8

import re, requests
from lxml import etree

def opengraph(*args, **kwargs):
    metadata = {}
    r = requests.get("http://www.facebook.com/Burninevent", stream=True)
    content = ""
    head = ""
    i = 0
    s = -1
    e = -1
    for chunk in r.iter_content(chunk_size=512):
        if chunk: # filter out keep-alive new chunks
            content += chunk
            if s != -1:
                e = chunk.find('</head>')
                if e != -1:
                    print "end %s" % e
                    head = content[i+s-7:i+e]
                    break
            else:
                s = chunk.find('<head>')
                print "start %s" % s
            i+=512


    print head
    # mime = magic.from_buffer(peek, mime=True)
    return metadata