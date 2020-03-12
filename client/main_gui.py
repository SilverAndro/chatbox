from tkinter import *

def build():
    root = Tk()
    root.title('Chatbox Main Menu')

    optionsFrame = Frame(root)

    nickLbl = Label(optionsFrame, text="Nick:", width=5)
    nickEntry = Entry(optionsFrame)
    nickLbl.pack(fill=X, side=LEFT)
    nickEntry.pack(fill=X, side=RIGHT, expand=1)

    optionsFrame.pack(fill=X)

    serverlist = Listbox(root, width=50)

    serverlist.pack(fill=BOTH, expand=1)

    joinbtn = Button(root, text="Join")
    joinbtn.pack(fill=X, side=BOTTOM)

    return root, nickEntry, serverlist, joinbtn
