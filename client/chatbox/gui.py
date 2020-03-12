from tkinter import *

def build():
    root = Tk()
    root.title('Chatbox Client')

    text = Text(root, wrap='word', state=DISABLED)
    text.pack(fill=BOTH, expand=1)

    text.tag_configure('important', background='#fff760')

    textinput = Entry(root)
    textinput.pack(fill=X)

    return root, text, textinput
