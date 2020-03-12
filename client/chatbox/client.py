import socket
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox

from chatbox.gui import build
from chatbox.packethandle import Protocol

def run(username, address):
    split = address.split(':')
    HOST, PORT = split[0], int(split[1])

    proto = Protocol()

    join = proto.build(b'\x00', username)

    root, chatlog, chatinput = build()

    def addMessage(decode):
        tag = "important" if decode[2] else "normal"
        chatlog.config(state=tk.NORMAL)
        chatlog.insert(tk.END, "{}: {}".format(decode[0], decode[1]), tag)
        chatlog.config(state=tk.DISABLED)

    def readloop(s):
        hasTaken = False
        active = True
        while active:
            try:
                try:
                    rec = s.recv(2048)
                    decode, rest = proto.read(rec)
                    pID = bytes([rec[0]])
                    if pID == b'\x03':
                        addMessage(decode)
                        if not hasTaken:
                            hasTaken = True
                            root.focus()
                            chatinput.focus()
                            print(root.focus_get())
                    if pID == b'\xfe':
                        addMessage(["Client", "Server closed.\n", True])
                    if pID == b'\xff':
                        addMessage(["Client", "Kicked by server, reason: {}\n".format(decode[0]), True])
                        active = False
                except socket.timeout:
                    None
            except ConnectionResetError:
                addMessage(["Client", "Server closed forcibly", True])
                active = False


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except:
            messagebox.showerror("Connection Error", "Could not connect to server!")
            print("Could not connect")
            sys.exit(0)

        s.settimeout(0.05)

        s.sendall(join)
        data = s.recv(2048)

        ret, more = proto.read(data)

        # Accepted
        if ret[0]:
            try:
                newthread = threading.Thread(
                    target=readloop, args=(s, ), daemon=True)
                newthread.start()

                def sendMsg(event):
                    msg = chatinput.get()
                    print(msg, len(msg), bytes(msg, "UTF-8"))
                    if len(msg) > 0:
                        chatinput.delete(0, last=tk.END)
                        pmsg = proto.build(b'\x02', msg + "\n")
                        s.send(pmsg)
                    return "break"

                chatinput.bind("<Return>", sendMsg)

                root.mainloop()
            except KeyboardInterrupt:
                print("Closed")
                sys.exit(0)
        else:
            print("Failed to login")
