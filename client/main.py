import threading
import tkinter as tk
import select
import socket
import struct

from main_gui import build
import chatbox.client as client

port = 4444
bufferSize = 1024
MCAST_GRP = '224.0.2.60'
knownAddresses = []

root, nick, serverlist, btn = build()

def handle_nick(event):
    if len(nick.get()) >= 18:
        return "break"
    if event.char.lower() not in 'abcdefghijklmnopqurstuvwxyz1234567890\x08\x07':
        return "break"

nick.bind("<Key>", handle_nick)

def listen():

    print("Starting listening")

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    s.bind(('', port))
    s.setblocking(0)

    while True:
        (read, written, exceptions) = select.select([s],[],[s], 0.5)
        for r in read:
            # Get data from buffer
            msg, peer = r.recvfrom(bufferSize)
            # Address is an (address, port) tuple
            address = peer[0]
            msg = msg.decode("utf-8")
            if msg.startswith("CHTBX|"):
                split = msg.split("|")
                adr = split[1]
                name = split[2]
                if not adr in knownAddresses:
                    serverlist.insert(tk.END, f"{name} - {adr}")
                    knownAddresses.append(adr)

listenThread = threading.Thread(target=listen, daemon=True)
listenThread.start()

def joinserver():
    log(None)

def log(event):
    selection = serverlist.curselection()
    if len(selection) > 0:
        serverAdr = serverlist.get(selection[0])
        serverAdr = serverAdr.split(" - ")[1]
        nickname = nick.get()
        if len(nickname) > 3:
            root.destroy()
            client.run(nickname, serverAdr)

serverlist.bind("<Double-Button-1>", log)

btn.config(command=joinserver)

root.mainloop()
