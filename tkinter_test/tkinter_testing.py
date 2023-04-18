import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import socket
import threading


class App(tk.Frame):
    def __init__(self, master, server_socket):
        super().__init__(master)

        self.auto_scroll_checkbox = None
        self.auto_scroll_flag = None
        self.name_label = None
        self.frm = None
        self.chatbox = None
        self.entry = None
        self.entry_contents = None
        self.quit_button = None

        self.server_socket = server_socket
        self.server_socket.connect((HOST, PORT))

        self.create_main_frame(master)
        self.create_name_label()
        self.create_entry()
        self.create_chat_box()
        self.create_quit_button()
        self.create_scroll_checkbox()

        self.create_listening_thread()

    def create_main_frame(self, master):
        self.frm = ttk.Frame(master, padding=5)
        self.frm.grid()

    def create_chat_box(self):
        self.chatbox = ScrolledText(self.frm, height=10, width=40, state="disabled")
        self.chatbox.grid(row=1, rowspan=3, column=0, columnspan=2)

    def create_entry(self):
        self.entry_contents = tk.StringVar()
        self.entry = tk.Entry(self.frm, width=20, textvariable=self.entry_contents)
        self.entry.grid(row=4, column=0, columnspan=1)
        self.entry.bind("<Key-Return>", self.print_entry)

    def create_quit_button(self):
        self.quit_button = tk.Button(self.frm, text="Quit", command=self.sign_out, width=5)
        self.quit_button.grid(row=4, column=1)

    def create_name_label(self):
        self.name_label = tk.Label(self.frm, text=socket.gethostname())
        self.name_label.grid(row=0, column=0)

    def create_scroll_checkbox(self):
        self.auto_scroll_flag = tk.BooleanVar()
        self.auto_scroll_checkbox = tk.Checkbutton(self.frm, text="Auto Scroll", variable=self.auto_scroll_flag)
        self.auto_scroll_checkbox.grid(row=0, column=1)

    def sign_out(self):
        self.server_socket.close()
        root.destroy()

    def print_entry(self, event):
        if not self.entry_contents.get():
            return

        self.server_socket.sendall(bytes(self.entry_contents.get(), 'utf-8'))
        self.entry_contents.set("")

    def create_listening_thread(self):
        threading.Thread(target=self.listen).start()

    def listen(self):
        while True:
            res = server_socket.recv(1024).decode()

            if not len(res):
                return

            self.update_chat_box(res)

    def update_chat_box(self, msg):
        self.chatbox["state"] = "normal"
        self.chatbox.insert('end', msg + "\n")
        self.chatbox["state"] = "disabled"
        if self.auto_scroll_flag.get():
            self.chatbox.see("end")


HOST, PORT = "0.0.0.0", 9999
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

root = tk.Tk()
myapp = App(root, server_socket)

myapp.mainloop()
