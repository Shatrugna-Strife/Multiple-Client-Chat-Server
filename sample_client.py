from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

first = True
name = ""

def receive():

    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg = msg
            msg_list.insert(tkinter.END, msg)
            msg_list.yview(tkinter.END)
            msg_list.xview()
        except OSError:
            break


def send(event=None):

    global first
    global name
    msg = my_msg.get()
    if first:
        name = msg
        my_msg.set("")
        client_socket.send(bytes(name, "utf8"))
        first = False
        return 0
    my_msg.set("")
    if msg == "{quit}":
        client_socket.send(bytes(msg, "utf8"))
        client_socket.close()
        root.quit()
        return 0
    client_socket.send(bytes(name+": "+msg, "utf8"))


def on_closing(event=None):
    my_msg.set("{quit}")
    send()

root = tkinter.Tk()
root.title("Group Chat")

messages_frame = tkinter.Frame(root)
my_msg = tkinter.StringVar()
my_msg.set("Type here.")
scrollbar_y = tkinter.Scrollbar(messages_frame)
scrollbar_x = tkinter.Scrollbar(messages_frame, orient = tkinter.HORIZONTAL)

msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
scrollbar_y.config(command = msg_list.yview)
scrollbar_x.config(command = msg_list.xview)
scrollbar_x.pack(side=tkinter.BOTTOM, fill=tkinter.X)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
scrollbar_y.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(root, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(root, text="Send", command=send)
send_button.pack()

root.protocol("WM_DELETE_WINDOW", on_closing)


# HOST = input('Enter host: ')
# PORT = input('Enter port: ')
HOST = ""
PORT = ""

if not HOST:
    HOST = "127.0.0.1"

if not PORT:
    PORT = 1234
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
