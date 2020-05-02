import sys
from tkinter import *
import os
import time
import ListSerialPorts as LSP 
import threading
from PIL import ImageTk, Image
import cv2 
import numpy as np

alt="15.69";
cdaalt="75.16";
supplyalt="150.2";
textsize="Times 70 bold"
textsize2="Times 20 bold"
    
    
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
    comval=' '

def setcomport(comportnum1):
    comportnumval=str(comportnum1)
    print(comportnumval)
    valkeeper.comval=comportnumval
    valkeeper.comtrue=True
    
    
def updateLable():
    if valkeeper.comtrue==True:
        cpnv=valkeeper.comval
        print('cpnv=')
        print( cpnv)
        LSP.mainscript(cpnv)
        valkeeper.comtrue=False
        valkeeper.comtrueLOOP=True
    if valkeeper.comtrueLOOP:
        print("working!!")
        ser_data_show()
    w.tk.after(1000,updateLable)
            

def ser_data_show():
    e=LSP.ColData()
    t1v.config(text=e[1])
    t2v.config(text=e[2])
    t3v.config(text=e[4])
    #alts.set(e[1])
    #supplyalts.set(e[2])
    #cdaalts.set(e[4])
    
    
def videocap():
    cap = cv2.VideoCapture(0) 
    if (cap.isOpened()== False):  
        print("Error opening video  file") 
    
    # Read until video is completed 
    while(cap.isOpened()):
        # Capture frame-by-frame 
        ret, frame = cap.read() 
        if ret == True: 
        
            # Display the resulting frame 
            cv2.imshow('Frame', frame) 
        
            # Press Q on keyboard to  exit 
            if cv2.waitKey(25) & 0xFF == ord('q'): 
                break
        
        # Break the loop 
        else:  
            break
    

if __name__ == '__main__':
    w = Fullscreen_Window()
    w.tk.geometry('1920x1000')
    w.tk.title("Assailing Falcon's Ground Station")
    w.tk.iconbitmap('icon1.ico')
    w.tk.configure(bg='black')
    
    

    x=LSP.ComFinder();

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
    File2.add_command(label="Select camera", command=w.tk.quit)


    
    #-------------------------------top frame------------------------------------
    topframe=PanedWindow(w.tk,bg="#000000")
    topframe.pack(side="top")
    topframe1=Label(topframe,bg='black')
    t1=Label(topframe1,text="Altitude:  ",font=textsize,bg='Green')
    t1.grid(row=0,column=0)
    t1v=Label(topframe1,text=alts,font=textsize,bg='Green')
    t1v.grid(row=0,column=1)
    t1xx=Label(topframe1,text="All Altitude values are in Feet(Ft)",font=textsize2,fg='Green',bg='black')
    t1xx.grid(row=1,column=0)
    centralBird=ImageTk.PhotoImage(Image.open('centralBird21.jpg'))
    tx0=Label(topframe1,text="Ft                  ",font=textsize,bg='black',fg='green').grid(row=0,column=9,columnspan=4)
    tx1=Label(topframe1,image=centralBird,bg='black').grid(row=0,column=10,columnspan=4,rowspan=2)
    t2=Label(topframe1,text="Supply Drop:",font=textsize,fg='#4166f5',bg='black')
    t2.grid(row=0,column=14,columnspan=4)
    t2v=Label(topframe1,text=supplyalts,font=textsize,fg='#4166f5',bg='black')
    t2v.grid(row=0,column=18)
    t3=Label(topframe1,text="CDA Drop:",font=textsize,fg='#4166f5',bg='black').grid(row=1,column=13,columnspan=4)
    t3v=Label(topframe1,text=cdaalts,font=textsize,fg='#4166f5',bg='black')
    t3v.grid(row=1,column=18)
    topframe.add(topframe1,width=1900)
    #thr1=threading.Thread(target=updateLable,args=())
    #thr1.start()
    updateLable()
    
    #-------------------------------middle frame---------------------------------
    photo=PhotoImage(file='splash.png')
    midframe=PanedWindow(w.tk,bg='blue')
    midframe.pack()
    midframeleft=Label(midframe)
    midframe1=Label(midframe)
    midframerigth=Label(midframe)
    #thr2=threading.Thread(target=videocap,args=())
    #thr2.start()
    
    m1=Label(midframe1,image=photo).pack()
    midframe.add(midframeleft,width=310,height=720)
    midframe.add(midframe1,width=1280,height=720)
    midframe.add(midframerigth,width=310,height=720)


    
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