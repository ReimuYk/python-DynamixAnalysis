import requests
import re
import pickle as pkl
import os

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
    while len(ret["No"])<3:
        ret["No"] = "0" + ret["No"]
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

def get_songlist():
    url = r"https://dynamixc4cat.fandom.com/wiki/Songs_by_BPM"
    data = requests.get(url)
    data = data.content.decode("UTF-8")
    txt = data.replace("\n","")
    txt = re.findall(r"wikitable(.+?)</table",txt)[0]
    songs = re.findall(r"tr>(.+?)</tr",txt)
    songs = songs[2:]
    for i in range(len(songs)):
        songs[i] = re.findall(r'href="(.+?)"',songs[i])[0]
        songs[i] = r"https://dynamixc4cat.fandom.com" + songs[i]
    return songs # urllist of songs

def download_songdata():
    for url in get_songlist():
        info = parse(url)
        print("No.%s download"%info["No"],end="\t")
        try:
            f = open("./song_data/%s.pkl"%info["No"],"wb")
            pkl.dump(info,f)
            f.close()
            print(info["title"])
        except:
            print("error in save")
            
def download_songpic():
    for filename in os.listdir("./song_data"):
        outname = filename.replace("pkl","png")
        if not os.path.exists("./song_data/%s"%outname):
            f = open("./song_data/%s"%filename,"rb")
            data = pkl.load(f)
            f.close()
            print(data["pic"])
            pic = requests.get(data["pic"])
            f = open("./song_data/%s"%outname,"wb")
            f.write(pic.content)
            f.close()

download_songpic()
            
    


##r = parse(testurl)
##print(r)
