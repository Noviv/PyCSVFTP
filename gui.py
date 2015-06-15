from Tkinter import *
from ftplib import FTP
from tempfile import mkstemp
from shutil import move
from os import remove, close
import csv
import fileinput
import os

#ret = -1
ret = 0
while ret != 0:
    #ip = raw_input('Server IP: ')
    ip = "ftp.gnu.org"
    ret = os.system('ping -n 1 -w 1000 ' + ip + '  >nul')
    if ret != 0:
        print "No response from IP address. Enter another."

#username = raw_input('Username: ')
username = "anonymous"
#password = raw_input('Password: ')
password = ""
#filename = raw_input('File path: ')#FILE PATH
filename = "data.txt"
#server_wd = raw_input('Server working directory: ')
server_wd = "/"

ftp = FTP(ip)
ftp.login()
ftp.cwd(server_wd)#SERVER WD
#with open(filename, 'r+') as file:
#    ftp.retrlines('retr ' + filename, file.write)

def replace(file_path, pattern, subst):
    fh, abs_path = mkstemp()
    with open(abs_path, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
		new_file.write(line.replace(pattern, subst))
    close(fh)
    remove(file_path)
    move(abs_path, file_path)

def numberchange(s1, s2, s3):
    x = 0
    for i in OPTIONS:
        if i != variable.get():
            x = x + 1
        else:
            break
    number.set(VALUES[x])

def getindex():
    x = 0
    for i in OPTIONS:
        if i != variable.get():
            x = x + 1
        else:
            return x

master = Tk()
master.title('Ez Params')
variable = StringVar(master)
variable.trace('w', numberchange)
number = StringVar(master)

statustext = 'FTP Active'
status = Label(master, text=statustext, anchor=W)
status.pack(side=BOTTOM, fill=X)

OPTIONS = []
VALUES = []

def loadValues():
    with open(filename, 'r+') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                OPTIONS.append(row[0])
                VALUES.append(row[1])                
    variable.set(OPTIONS[0])
    number.set(VALUES[0])
    e1 = apply(OptionMenu, (master, variable) + tuple(OPTIONS))

loadValues()

e1 = OptionMenu(master, variable, vars)
e1 = apply(OptionMenu, (master, variable) + tuple(OPTIONS))
e1.pack()
e1.focus_set()

e2 = Entry(master, textvariable=number)
e2.pack()
e2.focus_set()

def callback():
    orig = variable.get() + ',' +VALUES[getindex()]
    rep = variable.get() + ',' + e2.get()
    VALUES[getindex()] = e2.get()
    if orig != rep:
        statustext = 'Replacing in file...'
        replace(filename, orig, rep)#LOCAL WD
        statustext = 'FTPing over file...'
        with open(filename, 'r+') as file:
            print ftp.storlines('STOR ' + filename, file)
        loadValues()

b1 = Button(master, text="Send File", width=20, command=callback)
b1.pack()

def quitcall():
    ftp.close()
    master.destroy()
    sys.exit(0)

b2 = Button(master, text="Quit", width=20, command=quitcall)
b2.pack()

def restartcall():
    ftp.close()
    master.destroy()
    sys.exit(5)

b3 = Button(master, text="Restart", width=20, command=restartcall)
b3.pack()

master.update_idletasks()
w = master.winfo_screenwidth()
h = master.winfo_screenheight()
x = w/2 - 300/2
y = h/2 - 200/2
master.geometry("%dx%d%+d%+d" % (300, 200, x, y))
master.resizable(0, 0)

mainloop()
