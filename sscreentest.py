import sys
from tkinter import *
import os
import time
import ListSerialPorts as LSP 
import threading
from PIL import ImageTk, Image
import cv2 
import numpy as np
import PIL
from PIL import Image,ImageTk
import pytesseract

width, height = 1280, 720

alt="15.69";
cdaalt="75.16";
supplyalt="150.2";
textsize="Times 70 bold"
textsize2="Times 20 bold"
    
sroot = Tk()
sroot.minsize(height=1090,width=1920)
sroot.title("Splash window")
sroot.configure()
spath = "splash.png"
simg = ImageTk.PhotoImage(Image.open(spath))
my = Label(sroot,image=simg)
my.image = simg
my.place(x=0,y=0)
Frame(sroot,height=516,width=5,bg='black').place(x=520,y=0)
#lbl1 = Label(sroot,text="Welcome to Codersarts",font='Timesnewroman 20 ',fg='blue')
#lbl1.config(anchor=CENTER)
#lbl1.pack(padx = 100, pady = 100)
def call_mainroot():
    sroot.destroy()
    mainloopp()
sb=Button(sroot,text="Start Session",command=call_mainroot).pack()






def mainloopp():
    class Fullscreen_Window:

        def __init__(self):
            self.tk = Tk()
            #self.tk.attributes('-zoomed', True)  # This just maximizes it so we can see the window. It's nothing to do with fullscreen.
            self.frame = Frame(self.tk)
            self.frame.pack()
            self.state = False
            self.tk.bind("<F1>", self.toggle_fullscreen)
            self.tk.bind("<Escape>", self.end_fullscreen)
            self.tk.bind("<Q>", self.exit_program)
            self.tk.bind("<q>", self.exit_program)
            self.tk.bind("<R>", self.reset_send)
            self.tk.bind("<r>", self.reset_send)
            self.tk.bind("<C>", self.Cda_drop_send)
            self.tk.bind("<c>", self.Cda_drop_send)
            self.tk.bind("<H>", self.Supply_drop_send)
            self.tk.bind("<h>", self.Supply_drop_send)


        def toggle_fullscreen(self, event=None):
            self.state = not self.state  # Just toggling the boolean
            self.tk.attributes("-fullscreen", self.state)
            return "break"

        def end_fullscreen(self, event=None):
            self.state = False
            self.tk.attributes("-fullscreen", False)
            return "break"
        def exit_program(self,event=None):
            self.tk.quit()
        
        
        def reset_send(self,event=None):
            LSP.Send_reset()
        
        def Cda_drop_send(self,event=None):
            LSP.Drop_CDA()
        
        def Supply_drop_send(self,event=None):
            LSP.Drop_Supply()

    class valkeeper:
        comtrue=False
        comtrueLOOP=False
        camtrue=False
        comval=' '
        camval=0

    def setcomport(comportnum1):
        comportnumval=str(comportnum1)
        print(comportnumval)
        valkeeper.comval=comportnumval
        valkeeper.comtrue=True
    def camfinder():
        a=[]
        for device in range(10): 
            cap=cv2.VideoCapture(device)
            if (cap.isOpened()== True):  
                a.append(device) 
        print(a)
        return a 
    def setcamera(camnum):
        camnum=int(camnum)
        print(camnum)
        valkeeper.camtrue=True
        valkeeper.camval=camnum
        if(valkeeper.camtrue==True):
            print("in video")
            #valkeeper.camtrue=False
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            videocap()
           
    cap = cv2.VideoCapture(valkeeper.camval)
    def updateLable():
        if valkeeper.comtrue==True:
            cpnv=valkeeper.comval
            #print('cpnv=')
            #print( cpnv)
            LSP.mainscript(cpnv)
            valkeeper.comtrue=False
            valkeeper.comtrueLOOP=True
        if valkeeper.comtrueLOOP:
            #print("working!!")
            ser_data_show()
        w.tk.after(1000,updateLable)
                

    def ser_data_show():
        e=LSP.ColData()
        t1.config(text="Altitude:  "+e[1])
        t2.config(text="Supply Drop:"+e[2])
        t3.config(text="CDA Drop:"+e[4])
        #alts.set(e[1])
        #supplyalts.set(e[2])
        #cdaalts.set(e[4])
        
        
    def videocap():
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame=cv2.line(frame, (640,350), (640,370), (0,255,0),2)
        frame=cv2.line(frame, (630,360), (650,360), (0,255,0),2)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = PIL.Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        midframe1.imgtk = imgtk
        midframe1.configure(image=imgtk)
        vct=threading.Thread(target=midframe1.after,args=(10, videocap,))
        vct.start()

    if __name__ == '__main__':
        w = Fullscreen_Window()
        w.tk.geometry('1920x1000')
        w.tk.title("Assailing Falcon's Ground Station")
        w.tk.iconbitmap('icon1.ico')
        w.tk.configure(bg='black')
        
        

        x=LSP.ComFinder();
        cx=camfinder();
        alts=alt
    
        cdaalts=cdaalt
        
        supplyalts=supplyalt


        menu=Menu(w.tk)
        w.tk.config(menu=menu)
        File=Menu(menu)
        File1=Menu(menu)
        File2=Menu(menu)


    #-----------------------------File meneu--------------------------------------
        menu.add_cascade(label="File", menu=File)
        File.add_command(label="Full screen", command=w.toggle_fullscreen)
        File.add_command(label="End Fullscreen", command=w.end_fullscreen)
        File.add_separator()
        File.add_command(label="Exit", command=w.exit_program)

    #-----------------------------Comport meneu--------------------------------------
        menu.add_cascade(label="Com port", menu=File1)
        for i in x:
            File1.add_command(label=i,command=lambda:setcomport(i))


    #-----------------------------Camera meneu--------------------------------------
        menu.add_cascade(label="Camera", menu=File2)
        for j in cx:    
            File2.add_command(label=j, command=lambda:setcamera(j))


        
        #-------------------------------top frame------------------------------------
        topframe=PanedWindow(w.tk,bg="#000000")
        topframe.pack(side="top")
        topframe1=Label(topframe,bg='black')
        t1=Label(topframe1,text="Altitude:  "+alts,font=textsize,bg='Green')
        t1.grid(row=0,column=0)
        #t1v=Label(topframe1,text=alts,font=textsize,bg='Green')
        #t1v.grid(row=0,column=1)
        t1xx=Label(topframe1,text="All Altitude values are in Feet(Ft)",font=textsize2,fg='Green',bg='black')
        t1xx.grid(row=1,column=0)
        centralBird=ImageTk.PhotoImage(Image.open('centralBird21.jpg'))
        tx0=Label(topframe1,text="Ft                  ",font=textsize,bg='black',fg='green').grid(row=0,column=9,columnspan=4)
        tx1=Label(topframe1,image=centralBird,bg='black').grid(row=0,column=10,columnspan=4,rowspan=2)
        t2=Label(topframe1,text="Supply Drop:"+supplyalts,font=textsize,fg='#4166f5',bg='black')
        t2.grid(row=0,column=14,columnspan=4)
       # t2v=Label(topframe1,text=supplyalts,font=textsize,fg='#4166f5',bg='black')
       # t2v.grid(row=0,column=18)
        t3=Label(topframe1,text="CDA Drop:"+cdaalts,font=textsize,fg='#4166f5',bg='black')
        t3.grid(row=1,column=13,columnspan=4)
        #t3v=Label(topframe1,text=cdaalts,font=textsize,fg='#4166f5',bg='black')
        #t3v.grid(row=1,column=18)
        topframe.add(topframe1,width=1900)
        #thr1=threading.Thread(target=updateLable,args=())
        #thr1.start()
        updateLable()
        
        #-------------------------------middle frame---------------------------------
        photo=PhotoImage(file='splash.png')
        midframe=PanedWindow(w.tk,bg='blue')
        midframe.pack()
        midframe1=Label(midframe)
        #videocap()
        #thr2=threading.Thread(target=videocap,args=())
        #thr2.start()
        midframerigth=Label(midframe,bg="white")
        midframeleft=Label(midframe,bg="#696969")
        m1=Label(midframe1,image=photo).pack()
        midframe.add(midframeleft,width=310,height=720)
        midframe.add(midframe1,width=1280,height=720)
        midframe.add(midframerigth,width=310,height=720)
        startround=Button(midframeleft,text="Start Round Data recording",padx=2,pady=3,bg="green").pack()
        brec=Button(midframerigth,text="Record Video ",padx=2,pady=3,bg='Green').pack()

        
        #-------------------------------bottom frame---------------------------------
        botframe=PanedWindow(w.tk,bg='black')
        botframe.pack(side="bottom",pady=15)
        botframe1=Label(botframe,bg='black')
        bx0=Label(botframe1,text="                                                           ",font=textsize2,fg='black',bg='black').grid(row=0,column=0)
        cdadrop=Button(botframe1,text="Drop CDA",padx=2,pady=3,bg='Green',command=LSP.Drop_CDA).grid(row=0,column=1,padx=50,pady=1)
        bx1=Label(botframe1,text="                                               ",font=textsize2,fg='black',bg='black').grid(row=0,column=2,columnspan=5)
        supplydrop=Button(botframe1,text="Drop Supplies",padx=4,pady=3,bg='Green',command=LSP.Drop_Supply).grid(row=0,column=7,padx=50,pady=1)
        bx2=Label(botframe1,text="                                              ",font=textsize2,fg='black',bg='black').grid(row=0,column=8,columnspan=5)
        reset=Button(botframe1,text="Reset system",padx=7,pady=3,bg='red',command=LSP.Send_reset).grid(row=0,column=13,padx=50,pady=1)
        botframe.add(botframe1,width=1900)
        
        
        #-----------------------------------main loop----------------------------------
        w.tk.mainloop()
#def call_mainroot():
 #   sroot.destroy()
  #  mainloopp()

#sroot.after(1500,call_mainroot)         #TimeOfSplashScreen

sroot.mainloop()