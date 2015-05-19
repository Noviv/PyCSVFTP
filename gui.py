from Tkinter import *
from ftplib import FTP
from tempfile import mkstemp
from shutil import move
from os import remove, close
import csv
import fileinput

ip = raw_input('Server IP: ')
filename = raw_input('File path: ')#FILE PATH
server_wd = raw_input('Server working directory: ')
local_wd = raw_input('Local working directory: ')

ftp = FTP(ip)
ftp.login()
ftp.cwd(server_wd)#SERVER WD

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

status = Label(master, text='FTP Inactive', bd=1, relief=SUNKEN, anchor=W)
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
        print 'Replacing in file...'
        replace(local_wd + filename, orig, rep)#LOCAL WD
        print 'FTPing over file...'
        with open(filename, 'r+') as file:
            print ftp.storlines('STOR ' + filename, file)
        loadValues()

b1 = Button(master, text="Send to Robot", width=20, command=callback)
b1.pack()

def quitcall():
    ftp.close()
    master.quit
    exit()

b2 = Button(master, text="Quit", width=20, command=quitcall)
b2.pack()

master.update_idletasks()
w = master.winfo_screenwidth()
h = master.winfo_screenheight()
x = w/2 - 300/2
y = h/2 - 200/2
master.geometry("%dx%d%+d%+d" % (300, 200, x, y))
master.resizable(0, 0)

mainloop()
