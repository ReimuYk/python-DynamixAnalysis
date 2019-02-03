import requests
import re

##data = requests.get(r"https://dynamixc4cat.fandom.com/wiki/Stardust")
##data = data.content

testurl = r"https://dynamixc4cat.fandom.com/wiki/%E6%98%A5%E8%8F%8A"

def parse(url):
    data = requests.get(url)
    data = data.content
    ret = {}
    txts = re.findall("wikitable(.+?)table",data.decode("UTF-8").replace("\n",""))
    txt = txts[0]
    lines = re.findall(r"tr>(.+?)</tr",txt)
    ret["title"] = re.findall(r"b>(.+?)</b",lines[0])[0]
    ret["composer"] = re.findall(r"/>(.+?)</td",lines[0])[0]
    tds = re.findall(r'center">(.+?)</td',lines[2])
    ret["No"] = tds[0]
    ret["update"] = tds[1]
    ret["unlock"] = tds[2].replace(r"<br />","")
    ret["pic"] = re.findall(r'href="(.+?)"',lines[3])[0]
    ret["level"] = re.findall(r'center">(.+?)</td',lines[5])
    ret["notes"] = re.findall(r'center">(.+?)</td',lines[6])
    tds = re.findall(r'center">(.+?)</td',lines[8])
    ret["BPM"] = tds[0]
    ret["length"] = tds[1]
    ret["genre"] = tds[2]
    txt2 = txts[1]
    tds = re.findall(r'b>(.+?)</b',txt2)
    ret["leftside"] = tds[3]
    ret["rightside"] = tds[4]
    return ret

r = parse(testurl)
print(r)
