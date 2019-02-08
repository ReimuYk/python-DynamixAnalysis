import pickle as pkl
import os
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk

class GUI:
    def __init__(self):
        # load data
        self.data = self.load_songs()
        self.titles = self.title(self.data)
        # GUI grids
        self.root = Tk()
        self.root.geometry('555x450')
        self.root.title("Dynamix Data Viewer")
        # Search Line
        Label(self.root,text="Search:").place(x=30,y=30)
        self.searchtext = Entry(self.root,width=60)
        self.searchtext.place(x=100,y=33)
        # ListView content & event
        self.listframe = Frame(self.root,width=80)
        self.listview = ttk.Treeview(self.listframe,show="headings",height=16,columns=('No.','title'))
        self.listview.column('No.', width=80, anchor='center')
        self.listview.column('title', width=410, anchor='w')
        self.listview.heading('No.',text='No.')
        self.listview.heading('title',text='title')
##        dt = ['abcd','dd','lskdjf']
##        for i in range(3):
##            self.listview.insert('',i,values=(str(i),dt[i]))
        self.listview.bind("<Double-1>",self.DBclickList)
        self.listview.pack()
        self.listframe.place(x=30,y=80)
        # DataView
        self.dataframe = Frame(self.root,width=60)
        load = Image.open("./song_data/001.png")
        load = load.resize((320,180))
        render = ImageTk.PhotoImage(load)
        img = Label(self.dataframe,image=render)
        img.image = render
        img.grid(column=0,row=0,rowspan=8,columnspan=1)
        Label(self.dataframe,text="No.").grid(row=0,column=1)
        Label(self.dataframe,text="001",width=14).grid(row=0,column=2)
        Label(self.dataframe,text="Title").grid(row=1,column=1)
        Label(self.dataframe,text="Stardust").grid(row=1,column=2)
        Label(self.dataframe,text="Composer").grid(row=2,column=1)
        Label(self.dataframe,text="mmry").grid(row=2,column=2)
        Label(self.dataframe,text="BPM").grid(row=3,column=1)
        Label(self.dataframe,text="130").grid(row=3,column=2)
        Label(self.dataframe,text="length").grid(row=4,column=1)
        Label(self.dataframe,text="1:50").grid(row=4,column=2)
        Label(self.dataframe,text="Genre").grid(row=5,column=1)
        Label(self.dataframe,text="Trance").grid(row=5,column=2)
        Label(self.dataframe,text="Left").grid(row=6,column=1)
        Label(self.dataframe,text="MIXER").grid(row=6,column=2)
        Label(self.dataframe,text="Right").grid(row=7,column=1)
        Label(self.dataframe,text="PAD").grid(row=7,column=2)
        
        self.dataframe.place(x=30,y=80)
        
    def DBclickList(self,event):
        item = self.listview.selection()[0]
        print(self.listview.item(item,"values"))
        self.listframe.place_forget()
    def load_songs(self):
        files = []
        for name in os.listdir("./song_data"):
            if name[-3:] == "pkl":
                files.append(name)
        songs = []
        for pkldata in files:
            f = open("./song_data/%s"%pkldata,"rb")
            songs.append(pkl.load(f))
        return songs

    def title(self,songs):
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

    def search(self,reg,titles):
        ''' titles should be a list [] '''
        ret = []
        for t in titles:
            if reg.lower()==t[:len(reg)].lower():
                ret.append(t)
        return ret

g = GUI()



