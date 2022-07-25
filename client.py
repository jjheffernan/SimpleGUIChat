"""
    This is implemented as a package eventually intended for flask websites
"""
import socket
import threading
from tkinter import *
import tkinter.scrolledtext
from tkinter import font
from tkinter import ttk

# from tkinter import simpledialog
# import sys
import os
# Set environment variable
os.environ['TK_SILENCE_DEPRECATION'] = '1'

# declaring network as constants
HOST = '127.0.0.1'  # localhost port
PORT = 9090  # manual port declaration
ADDRESS = (HOST, PORT)
# nothing below 1024 unless root


# formatting
FORMAT = 'utf-8'
BG_GRAY = '#AAB2B9'
BG_COLOR = '#17202A'
TEXT_COLOR = '#EAECEE'

FONT = 'Helvetica 14'
FONT_BOLD = 'Helvetica 13 bold'

# local list of other clients
# clients = []
# nicknames = []
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

# class Client:
#
#     def __init__(self, host, port):
#
#         # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         # self.sock.connect((host, port))
#
#         # opens pop-up.
#         msg = tkinter.Tk()
#         msg.withdraw()  # not best practices
#
#         # self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=msg)
#         self.nickname = 'foo'
#
#
#         # flag to allow GUI open
#         self.gui_done = False
#         # flag to end GUI
#         self.running = True
#
#         # gui interactive thread
#         #
#         # gui_thread = threading.Thread(target=self.gui_loop)  # looks like crash happens here
#         # deals with server connection
#         receive_thread = threading.Thread(target=self.receive)
#
#         # gui_thread.start()
#         # self.gui_loop()
#         receive_thread.start()
#         self.win.mainloop()
#
#     # FIX THE CANCEL BUTTON
#     # front end for chat interface
#     # must be built out, then built into web forum
#     # add getnickname method
#
#         # self.win.mainloop()
#         # try this as last line call
#         # pass
#
#     def write(self):
#         message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}" # weird syntax, be sure to read up
#         # can change message function to be server side
#         # better implementation to get message and then assign nick via DB
#         self.sock.send(message.encode('utf-8'))
#         self.input_area.delete('1.0', 'end')
#         # pass
#
#     def stop(self):
#         self.running = False
#         self.win.destroy()
#         self.sock.close()
#         exit(0)
#         # pass
#
#     def receive(self):
#         while self.running:
#             try:
#                 message = self.sock.recv(1024)  # 1024 bytes
#                 if message == 'NICK':
#                     self.sock.send(self.nickname.encode('utf-8'))
#                 else:
#                     if self.gui_done:
#                         self.text_area.config(state='normal')
#                         self.text_area.insert('end', message)
#                         self.text_area.yview('end') # pulls view down to end
#                         self.text_area.config(state='disabled')
#
#             except ConnectionAbortedError:
#                 print("Connection aborted.")
#                 break
#             except ConnectionRefusedError:
#                 print("Server is not active.")
#                 break
#             except Exception as e:
#                 print("Unknown Error", e)
#                 self.sock.close()
#                 break
#                 # pass
#         # pass


class GUI:
    # improved constructor method for GUI
    def __init__(self):

        # un-hide chat window
        self.Window = tkinter.Tk()
        self.Window.configure(background=BG_GRAY)
        self.Window.withdraw()

        # login window
        self.login = tkinter.Toplevel()
        # set title
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)

        # create a Label
        self.pls = tkinter.Label(self.login, text="Please login to continue", justify='center', font="Helvetica 14 bold")

        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)
        # create a Label
        self.labelName = tkinter.Label(self.login, text="Name: ", font="Helvetica 12")
        self.labelName.place(relheight=0.2, relx=0.1, rely=0.2)

        # create a entry box for
        # tyoing the message
        self.entryName = tkinter.Entry(self.login, font="Helvetica 14")

        self.entryName.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)

        # set the focus of the cursor
        self.entryName.focus()

        # create a Continue Button
        # along with action
        self.go = tkinter.Button(self.login, text="CONTINUE", font="Helvetica 14 bold",
                                 command=lambda: self.goAhead(self.entryName.get()))

        self.go.place(relx=0.4, rely=0.55)
        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)

        # the thread to receive messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()

    # The main layout of the chat
    def layout(self, name):
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550, bg=BG_COLOR)
        self.labelHead = tkinter.Label(self.Window, bg=BG_COLOR, fg=TEXT_COLOR, text=self.name,
                                       font=FONT_BOLD, pady=5)

        self.labelHead.place(relwidth=1)
        self.line = tkinter.Label(self.Window, width=450, bg=BG_GRAY)

        self.line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.textCons = tkinter.Text(self.Window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                     font=FONT, padx=5, pady=5)

        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)

        self.labelBottom = tkinter.Label(self.Window, bg=BG_GRAY, height=80)

        self.labelBottom.place(relwidth=1, rely=0.825)

        self.entryMsg = tkinter.Entry(self.labelBottom, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)

        self.entryMsg.focus()

        # create a Send Button
        self.buttonMsg = tkinter.Button(self.labelBottom, text="Send", font="Helvetica 10 bold", width=20, bg=BG_GRAY,
                                        command=lambda: self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = tkinter.Scrollbar(self.textCons)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1, relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state='disabled')

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state='disabled')
        self.msg = msg
        self.entryMsg.delete(0, 'end')
        send = threading.Thread(target=self.send_message)
        send.start()

    # function to receive messages
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)

                # if the messages from the server is NAME send the client's name
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                else:
                    # insert messages to text box
                    self.textCons.config(state='normal')
                    self.textCons.insert('end',
                                         message + "\n\n")

                    self.textCons.config(state='disabled')
                    self.textCons.see('end')
            except:
                # an error will be printed on the command line or console if there's an error
                print("An error occurred!")
                client.close()
                break

    # function to send messages
    def send_message(self):
        self.textCons.config(state='disabled')
        while True:
            message = f"{self.name}: {self.msg}"
            client.send(message.encode(FORMAT)) # something goes wrong here that causes bad file desciptor
            break

    # def gui_loop(self):
    #     self.win = tkinter.Tk() # remove any IO from constructor
    #     self.win.configure(bg="grey")  # to configure window
    #
    #     self.chat_label = tkinter.Label(self.win, text="Chat:", bg="grey")
    #     self.chat_label.config(font=("Arial", 12))
    #     self.chat_label.pack(padx=20, pady=5)
    #
    #     self.text_area = tkinter.scrolledtext.ScrolledText()
    #     self.text_area.pack(padx=20, pady=5)
    #     self.text_area.config(state='disabled')  # bad implementation
    #     # when state = disabled, cannot change content
    #     # needs to be state= default, then make the change, then enabled
    #
    #     self.msg_label = tkinter.Label(self.win, text="Message:", bg="lightgray")
    #     self.msg_label.config(font=("Arial", 12))
    #     self.msg_label.pack(padx=20, pady=5)
    #
    #     self.input_area = tkinter.Text(self.win, height=3)
    #     self.input_area.pack(padx=20, pady=5)
    #
    #     self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
    #     self.send_button.config(font=("Arial", 12))
    #     self.input_area.pack(padx=20, pady=5)
    #
    #     self.gui_done = True
    #     # try to pull gui configuration from templates
    #     self.win.protocol("WM_DELETE_WINDOW", self.stop)


# def main(sys.argv):
#     if len(sys.argv) != 3:
#         print('Using default gateway')


# starts client connection
if __name__ == '__main__':
    # main()
    # setup connection
    # client = Client(HOST, PORT)
    # render GUI
    # Client.gui_loop()
    g = GUI()
# wrap in if
