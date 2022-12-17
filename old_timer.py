from tkinter import *
import time as tm
from datetime import timedelta
from tkinter import messagebox
from winsound import *
import sqlite3
# from PIL import Image, ImageTk

"""passw  = password"""

window = Tk()
window.title('Tomato Timer')

window.iconbitmap(r'tomato.ico')
# window.geometry('485x275')
window.resizable(0, 0)
window.configure(bg="black")

# study_time = 20 * 60
study_time = 3
rest_time = 3
counter_top = timedelta(seconds=study_time)  # convert integer into time
print(counter_top)

tomatos_eraned = 0

rest_counter = False
study_counter = True
down_counter = True

subjectOption = StringVar()

play = lambda: PlaySound("click_one.wav", SND_FILENAME)

studies = ["general", "math"]

global counter_label


def display_time():
    current_time = tm.strftime('%H:%M:%p')
    clock_label['text'] = current_time
    window.after(1000, display_time)  # corrects the lost of 1ms per second calling ...


# TASK: add sound to the time up
# def play():
#     return PlaySound("click_one.wav", SND_FILENAME)


def popout():
    global study_counter
    global tomatos_eraned

    if study_counter:

        messagebox.showwarning("Time up!", "You erned a tomato!!", icon="info")
        response = messagebox.askquestion("Ready?", "continue to rest?", icon="question")
        if response == "yes":
            study_countdown(rest_time)
            study_counter = False
            tomatos_eraned *= 1
    else:
        messagebox.showwarning("Time up!", "You Lazy bastard!!", icon="info")
        response = messagebox.askquestion("Ready?", "Earn 1 more tomato?", icon="question")

        if response == "yes":
            study_countdown(rest_time)
            study_counter = True


def subject_panel():
    top = Toplevel(bg='black')
    top.iconbitmap(r'tomato.ico')

    entry = Entry(top)
    entry.pack()
    entry.insert(0, "Enter new subject")
    sudmit = Button(top, text="add", command=add_subject)
    sudmit.pack()


def study_countdown(time=0):
    global study_counter
    global counter_label

    if not time:
        global study_time
        global rest_time
    else:
        study_time = time  # * 60

    mins, secs = divmod(study_time, 60)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    counter_label['text'] = timeformat

    study_time -= 1

    if study_time == 0:
        counter_label['text'] = "00:00"
        # study_counter = False
        popout()
        return 0

    window.after(1000, study_countdown)


def add_subject():
    global studies
    global entry

    studies.append(entry.get())
    entry.delete(0, END)


def display_gadgets():
    global clock_label
    global counter_label

    clock_label = Label(window, font='ariel 80', bg='black', fg='red')
    clock_label.grid(row=0, column=0, columnspan=3)

    counter_label = Label(window, text="00:00", font='ariel 80', bg='black', fg='red')
    counter_label.grid(row=1, column=0, columnspan=3)

    start = Button(window, text="start", command=study_countdown)
    start.grid(sticky="w")

    study_entry_label = Label(window, text="Study Time", fg="white", bg="black")
    study_entry_label.grid(row=2, column=1, sticky="e")

    study_entry = Entry(window, width=5)
    study_entry.grid(row=2, column=2, sticky="w")

    rest_entry_label = Label(window, text="Rest Time", fg="white", bg="black")
    rest_entry_label.grid(row=2, column=3, sticky="e")

    rest_entry = Entry(window, width=5)
    rest_entry.grid(row=2, column=4, sticky="w")

    add_subject = Button(window, text='edit_subjects', command=subject_panel)
    add_subject.grid(row=0, column=3, sticky="n")

    #  Task: tomato design UI

    # load = Image.open("tomato.ico")
    # render = ImageTk.PhotoImage(load)
    # img = Label(window, image=render, bg="black", width=100, height=100)  #
    # img.image = render
    # img.grid(row=3, column=0, sticky="w")


def display_subjects():
    frame1 = Frame(window, bg='black')
    frame1.grid(row=0, column=3)
    row = 0

    for subject in studies:
        radio = Radiobutton(frame1, bg="black")
        radio.grid(row=row, column=0, sticky="e")
        radio.configure(variable=subjectOption, value=subject)

        #  TASK: deselect the radio buttons, general selected by default

        label = Label(frame1, text=subject, bg="black", fg="white")
        label.grid(row=row, column=1, sticky="w")
        row += 1


class Database:

    def __init__(self, db, username):
        self.username = username
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {username}_studies (id INTEGER PRIMARY KEY, subject text, tomatos text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute(f'SELECT * FROM {self.username}_studies')
        rows = self.cur.fetchall
        return rows

    def insert(self, subject, tomatos):
        self.cur.execute(f"INSERT INTO {self.username}_studies VALUES (NULL, ?, ?)", (subject, tomatos))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute(f"DELETE FROM {self.username}_studies WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, part, customer, retailer, price):
        self.cur.execute(f'UPDATE {self.username}_studies SET subject = ?, tomatos =? WHERE id = ?',
                         (part, customer, retailer, price, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()


display_gadgets()
display_time()
display_subjects()

window.mainloop()
