import pickle as pkl
import os

def load_songs():
    files = []
    for name in os.listdir("./song_data"):
        if name[-3:] == "pkl":
            files.append(name)
    songs = []
    for pkldata in files:
        f = open("./song_data/%s"%pkldata,"rb")
        songs.append(pkl.load(f))
    return songs

def title(songs):
    ret = {"ASC":[],"OTH":[]}
    def IS_ASCII(string):
        for c in string:
            if not (( c>="a" and c<="z") or ( c>="A" and c<="Z") or c==" "):
                return False
        return True
    for s in songs:
        t = s["title"]
        if IS_ASCII(t[:3]):
            ret["ASC"].append(t)
        else:
            ret["OTH"].append(t)
    return ret

def search(reg,titles):
    ''' titles should be a list [] '''
    ret = []
    for t in titles:
        if reg.lower()==t[:len(reg)].lower():
            ret.append(t)
    return ret

data = load_songs()
ts = title(data)


