import serial.tools.list_ports
import serial
import re

def ComFinder():
     c=list(serial.tools.list_ports.comports())
     a= [item[0] for item in c]
     return a



s=False

def mainscript(Comportnum):
     global ser
     ser = serial.Serial(
     port=Comportnum,
     baudrate=57600
     )
     global s
     s=ser.isOpen()
     print(ser.isOpen())
     print('serial is open')
def ColData():
     while s==True:
          d=ser.readline().decode("utf-8")
          #print(d)
          e=re.split('%',d)
          print(e)
          ser.write('D'.encode('utf-8'))
          return e
   

def Drop_Supply():
     ser.write('H'.encode('utf-8'))
     print('H')

def Drop_CDA():
     ser.write('S'.encode('utf-8'))
     print('S')

def Send_reset():
     ser.write('R'.encode('utf-8'))
     print('R')