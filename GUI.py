import pickle as pkl
import win32api
import win32con
import os
from TkinterDnD2 import *
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk

testsongdata = {'genre': 'Dancecore', 'level': ['2', '6', '9', '-', '14'], 'composer': 'SUWAKI', 'BPM': '171', 'rightside': 'PAD', 'No': '002', 'title': '春菊', 'length': '2:17', 'unlock': 'Rank 1 + 23000 Frags', 'pic': 'https://vignette.wikia.nocookie.net/dynamixc4cat/images/9/9a/%E6%98%A5%E8%8F%8A.jpg/revision/latest?cb=20141126084307', 'update': '30/10/2014', 'notes': ['208', '601', '719', '-', '1206'], 'leftside': 'MIXER'}


class GUI:
    def __init__(self):
        # load data
        self.data = self.load_songs()
        self.titles = self.title(self.data)
        # GUI grids
        self.root = TkinterDnD.Tk()
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>",self.event_drop)
        self.root.geometry('555x450')
        self.root.title("Dynamix Data Viewer")
        # Search Line
        Label(self.root,text="Search:").place(x=30,y=30)
        self.searchcontent = StringVar()
        self.searchtext = Entry(self.root,textvariable=self.searchcontent,width=60)
        self.searchtext.bind("<Return>",self.searchresult)
        self.searchtext.place(x=100,y=33)
        # ListView content & event
        self.listframe = Frame(self.root,width=80)
        self.listview = ttk.Treeview(self.listframe,show="headings",height=16,columns=('No.','title'))
        self.listview.column('No.', width=80, anchor='center')
        self.listview.column('title', width=410, anchor='w')
        self.listview.heading('No.',text='No.')
        self.listview.heading('title',text='title')
        # add listview data
        self.listview.bind("<Double-1>",self.DBclickList)
        self.listview.pack()
        self.listframe.place(x=30,y=80)
        # displayfile (picture)
        self.displayfile = StringVar()

    def event_drop(self,event):
        print(event.data)
        filepath, ext = os.path.splitext(event.data)
        if not ext in ['.jpg','.png','.jpeg']:
            print("The file is not a picture")
            return
        
        load = Image.open(event.data)
        load = load.resize((500,282))
        render = ImageTk.PhotoImage(load)
        img = Label(self.root,image=render)
        img.image = render
        img.place(x=585,y=30)
        
        self.displayfile.set(event.data)
        
    def searchresult(self,event):
        try:
            self.dataframe.place_forget()
        except:
            pass
        try:
            self.listframe.place_forget()
        except:
            pass
        
        # clear list
        for item in self.listview.get_children():
            self.listview.delete(item)
            
        # add content
        if self.searchcontent.get()=='#':
            listdata = self.titles["OTH"]
        else:
            listdata = self.search(self.searchcontent.get(),self.titles["ASC"])
        idx=1
        for line in listdata:
            self.listview.insert("",idx,text="",values=line)
            idx+=1
        self.listframe.place(x=30,y=80)
        
    def display(self,songdata):
        try:
            self.dataframe.place_forget()
        except:
            pass
        try:
            self.listframe.place_forget()
        except:
            pass
        # DataView
        self.dataframe = Frame(self.root,width=60)
        load = Image.open("./song_data/%s.png"%songdata["No"])
        load = load.resize((320,180))
        render = ImageTk.PhotoImage(load)
        img = Label(self.dataframe,image=render)
        img.image = render
        img.grid(column=0,row=0,rowspan=8,columnspan=1)
        Label(self.dataframe,text="No.").grid(row=0,column=1)
        Label(self.dataframe,text=songdata["No"],width=14).grid(row=0,column=2)
        Label(self.dataframe,text="Title").grid(row=1,column=1)
        Label(self.dataframe,text=songdata["title"]).grid(row=1,column=2)
        Label(self.dataframe,text="Composer").grid(row=2,column=1)
        Label(self.dataframe,text=songdata["composer"]).grid(row=2,column=2)
        Label(self.dataframe,text="BPM").grid(row=3,column=1)
        Label(self.dataframe,text=songdata["BPM"]).grid(row=3,column=2)
        Label(self.dataframe,text="length").grid(row=4,column=1)
        Label(self.dataframe,text=songdata["length"]).grid(row=4,column=2)
        Label(self.dataframe,text="Genre").grid(row=5,column=1)
        Label(self.dataframe,text=songdata["genre"]).grid(row=5,column=2)
        Label(self.dataframe,text="Left").grid(row=6,column=1)
        Label(self.dataframe,text=songdata["leftside"]).grid(row=6,column=2)
        Label(self.dataframe,text="Right").grid(row=7,column=1)
        Label(self.dataframe,text=songdata["rightside"]).grid(row=7,column=2)
        self.scoreframe = Frame(self.dataframe,bg="white")
        difflist = ["Casual","Normal","Hard","Mega","Giga"]
        colorlist= ["#C1FFC1","#CAE1FF","#EEB4B4","#EE82EE","#DCDCDC"]
        Label(self.scoreframe,text="难度",width=10,bg="white").grid(row=0,column=0)
        Label(self.scoreframe,text="等级",width=6).grid(row=0,column=1)
        Label(self.scoreframe,text="分数",width=15,bg="white").grid(row=0,column=2)
        Label(self.scoreframe,text="Perfect",width=10).grid(row=0,column=3)
        Label(self.scoreframe,text="Good",width=10,bg="white").grid(row=0,column=4)
        Label(self.scoreframe,text="Miss",width=10).grid(row=0,column=5)
        Label(self.scoreframe,text="STAT",width=4,bg="white").grid(row=0,column=6)
        
        class EditableCell:
            def __init__(self,frm,linkfile,r,c,color,w):
                self.frm = frm
                self.linkfile = linkfile
                self.r = r
                self.c = c
                self.color=color
                self.w = w
                self.data = StringVar()
                f = open(self.linkfile,"r")
                self.data.set(eval(f.read())[r][c])
                f.close()
                self.cell = Label(self.frm,textvariable=self.data,bg=self.color)
                self.cell.bind("<1>",self.edit)
                self.cell.grid(row=self.r,column=self.c,sticky=W+E)
            def edit(self,event):
                self.cell.grid_forget()
                self.cell = Entry(self.frm,textvariable=self.data,width=self.w,justify='center')
                self.cell.bind("<Return>",self.save)
                self.cell.grid(row=self.r,column=self.c,sticky=W+E)
            def save(self,event):
                self.cell = Label(self.frm,textvariable=self.data,bg=self.color)
                self.cell.bind("<1>",self.edit)
                self.cell.grid(row=self.r,column=self.c,sticky=W+E)
                f = open(self.linkfile,"r")
                dt = eval(f.read())
                f.close()
                dt[self.r][self.c] = self.data.get()
                f = open(self.linkfile,"w")
                f.write(str(dt))
                f.close()
            def value(self):
                f = open(self.linkfile,"r")
                dt = eval(f.read())
                f.close()
                return dt[self.r][self.c]
        
        class StatCell:
            def __init__(self,frm,linkfile,r,c,color,datacells,displayfile):
                self.frm = frm
                self.linkfile = linkfile
                self.r = r
                self.c = c
                self.color = color
                self.st = st
                self.datacells = datacells # 4 cells ['score','perfect','good','miss']
                self.displayfile = displayfile # StringVar()
                self.cell = None
            def refresh(self):
                try:
                    self.cell.grid_forget()
                except:
                    pass
                d = self.datacells
                if d[0]=='1000000':
                    self.st = 'Ω'
                elif d[3]=='0':
                    self.st = 'FC'
                elif d[0]!='' and d[1]!='' and d[2]!='' and d[3]!='':
                    self.st = 'CL'
                else:
                    self.st = 'NP'
                self.cell = Label(self.frm,text=self.st,bg=self.color)
                self.cell.grid(row=self.r,column=self.c,sticky=W+E)
            def event_rightclick(self,event):
                # replace linkfile if file loaded
                pass
                

        if not os.path.exists("./user_data/%s.json"%songdata["No"]):
            f = open("./user_data/%s.json"%songdata["No"],"w")
            f.write(str([['']*7]*6))
            f.close()
        for diffnum in range(5):
            if songdata["level"][diffnum]=='-':
                Label(self.scoreframe,bg="white").grid(row=1+diffnum,columnspan=7)
            else:
                Label(self.scoreframe,text=difflist[diffnum],bg=colorlist[diffnum]).grid(row=1+diffnum,column=0,sticky=W+E)
                Label(self.scoreframe,text=songdata["level"][diffnum],bg=colorlist[diffnum]).grid(row=1+diffnum,column=1,sticky=W+E)
                celllist = []
                celllist.append(EditableCell(self.scoreframe,"./user_data/%s.json"%songdata["No"],diffnum+1,2,colorlist[diffnum],15))
                for k in range(3,6):
                    celllist.append(EditableCell(self.scoreframe,"./user_data/%s.json"%songdata["No"],diffnum+1,k,colorlist[diffnum],10))
                

        Label(self.dataframe).grid(row=8)
        self.scoreframe.grid(row=9,column=0,columnspan=3,sticky=W+E)
        self.dataframe.place(x=30,y=80)
        
    def DBclickList(self,event):
        item = self.listview.selection()[0]
        number = self.listview.item(item,"values")[0]
        self.listframe.place_forget()
        for song in self.data:
            if song["No"]==number:
                self.display(song)
                break
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
                ret["ASC"].append((s["No"],t))
            else:
                ret["OTH"].append((s["No"],t))
        return ret

    def search(self,reg,titles):
        ''' titles should be a list [(No,title)] '''
        ret = []
        for t in titles:
            if reg.lower()==t[1][:len(reg)].lower():
                ret.append(t)
        return ret

g = GUI()



