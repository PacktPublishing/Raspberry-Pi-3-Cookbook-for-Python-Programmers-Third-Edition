#!/usr/bin/python3
# graphicmenu.py
import tkinter as tk
from subprocess import call
import threading

#Define applications ["Display name","command"]
leafpad = ["Leafpad","leafpad"]
scratch = ["Scratch","scratch"]
pistore = ["Pi Store","pistore"]
app_list = [leafpad,scratch,pistore]
APP_NAME = 0
APP_CMD  = 1

class runApplictionThread(threading.Thread):
    def __init__(self,app_cmd):
        threading.Thread.__init__(self)
        self.cmd = app_cmd
    def run(self):
        #Run the command, if valid
        try:
            call(self.cmd)
        except:
            print ("Unable to run: %s" % self.cmd)

class appButtons:
    def __init__(self,gui,app_index):
        #Add the buttons to window
        btn = tk.Button(gui, text=app_list[app_index][APP_NAME],
                        width=30, command=self.startApp)
        btn.pack()
        self.app_cmd=app_list[app_index][APP_CMD]
    def startApp(self):
        print ("APP_CMD: %s" % self.app_cmd)
        runApplictionThread(self.app_cmd).start()       

root = tk.Tk()
root.title("App Menu")
prompt = '      Select an application      '
label1 = tk.Label(root, text=prompt, width=len(prompt), bg='green')
label1.pack()
#Create menu buttons from app_list
for index, app in enumerate(app_list):
    appButtons(root,index)
#Run the tk window
root.mainloop()
#End