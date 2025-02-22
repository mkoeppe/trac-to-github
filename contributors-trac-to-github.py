# Adapted from scripts/geocode.py

import certifi
import urllib3
import pprint

from xml.dom.minidom import parseString

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where()
)

ack = parseString(http.request('GET', 'https://raw.githubusercontent.com/sagemath/website/master/conf/contributors.xml').data.decode('utf-8'))

usernames = {}

for c in ack.getElementsByTagName("contributors")[0].childNodes:
    if c.nodeType != ack.ELEMENT_NODE:
        continue
    if c.tagName != "contributor":
        continue
    trac = c.getAttribute("trac")
    github = c.getAttribute("github")
    if trac:
        for t in trac.split(','):
            t = t.strip()
            if t:
                if github:
                    usernames[t] = github
                elif t not in usernames:
                    usernames[t] = None

pprint.pp(usernames)


print('# Trac accounts without github account: ' + ','.join(
    t for t, g in usernames.items() if not g))
