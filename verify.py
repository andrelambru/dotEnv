# THIS IS CRAP CODE!

import requests


s = requests.Session()
IPs = []
for _ in open("good.txt", "r").readlines():
    IPs.append(_.strip())


skip = ["<html", "<htm", "<script", "<image", "<title", "<div", "<b", "<p", "<h1", "<h3", "<expired", "<xml", "<?xml"]
for _ in IPs:
    bad = False
    try:
        r = s.get(_.strip(), timeout=5)
        for sk in skip:
            if sk in r.text or sk.upper() in r.text:
                print("[BAD] " + _)
                bad = True
                break
        if bad:
            continue

        if "=" in r.text:
            print("[HIT] " + _)
            print(_, file=open("verified.txt", "a"))
        else:
            print(r.text)
    except:
        pass