#!/usr/bin/python

import sys
import urllib
import re
import json
from BeautifulSoup import BeautifulSoup

cache = {}

for line in open(sys.argv[1]):
    fields = line.rstrip('\n').split('\t')
    sid = fields[0]
    uid = fields[1]

    url = 'http://twitter.com/%s/status/%s' % (uid, sid)
    #print url

    text = "Not Available"
    if cache.has_key(sid):
        text = cache[sid]
    else:
        soup = BeautifulSoup(urllib.urlopen(url))
        for j in soup.findAll("input", "json-data", id="init-data"):
            js = json.loads(j['value'])
            if(js.has_key("embedData")):
                text = js["embedData"]["status"]["text"]
                cache[sid] = text
                break
    print "\t".join(fields + [text])
