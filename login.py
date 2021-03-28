##@nil gaikwad
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import sqlite3
import os

from subprocess import call
speech="Welcome admin "
call(["espeak",speech])

# FRAME
def quit(*args):
    root.destroy()


root = Tk()
root.attributes("-fullscreen", True)
root.configure(background='black')
root.bind("<Escape>", quit)
root.bind("x", quit)

def Database():
    global conn, cursor
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS user (u_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT, password TEXT)")
    cursor.execute("SELECT * FROM user WHERE `username` = 'anil' AND `password` = '2020'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO user (username, password) VALUES('anil', '2020')")
        conn.commit()


label = Label(root)
label.pack()


# Login Page
def Login(event=None):
    Database()
    if USERNAME.get() == "" or PASSWORD.get() == "":
        lbl_text.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM user WHERE `username` = ? AND `password` = ?",
                       (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            Home2()

            USERNAME.set("")
            PASSWORD.set("")
            lbl_text.config(text="")
        else:
            lbl_text.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")
    cursor.close()
    conn.close()
# First Pop up
def Home2():
    os.system('python3 second1.py')

# variable
USERNAME = StringVar()
PASSWORD = StringVar()

# frames
Top = Frame(root, bd=10, relief=RIDGE)
Top.pack(side=TOP, fill=X)
Falt = Frame(root, height=500, relief=RIDGE)
Falt.pack(side=TOP, fill=X, ipady=50, ipadx=200)
Form = Frame(root, height=50, bd=30)
Form.pack(side=TOP, pady=20)

# lable
lbl_title = Label(Top, text="Welcome Admin", bg="black", fg="green", font=('arial', 44))
lbl_title.pack(fill=BOTH, expand=1)

cre = Label(Falt, text="Enter your credentials ", fg="green", bg="black", font=('arial', 20))
cre.pack(fill=BOTH, expand=1)

lbl_username = Label(Form, text="Username:", font=('arial', 16), bd=15)
lbl_username.grid(row=0, sticky="e")
lbl_password = Label(Form, text="Password:", font=('arial', 16), bd=15)
lbl_password.grid(row=1, sticky="e")
lbl_text = Label(Form)
lbl_text.grid(row=2, columnspan=2)

#ENTRY
username = Entry(Form, textvariable=USERNAME, font=(16))
username.grid(row=0, column=1)
password = Entry(Form, textvariable=PASSWORD, show="*", font=(16))
password.grid(row=1, column=1)

# BUTTON
btn_login = Button(Form, text="Login", width=25, command=Login, font=('arial', 14))
btn_login.grid(pady=25, row=6, columnspan=5)
btn_login.bind("<Return>", quit)

#main
if __name__ == '__main__':
    mainloop()

##end 
