from tkinter import *
import math
import time as tm

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
CHECKED = "✔"
WORK_MIN = 1  # 25
SHORT_BREAK_MIN = 1  # 5
LONG_BREAK_MIN = 1  # 20

reps = 0
my_timer = None


# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    global reps

    window.after_cancel(my_timer)
    canvas.itemconfig(timer_text, text='00:00')
    label_top.configure(text='Timer')
    label_bottom.configure(text='')
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    global reps
    reps += 1

    work_secs = WORK_MIN * 60
    short_break_secs = SHORT_BREAK_MIN * 60
    long_break_secs = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_secs)
        label_top.configure(text="Break", fg=RED)

    elif reps % 2 == 0:
        count_down(short_break_secs)
        label_top.configure(text="5 mins Break", fg=PINK)
    else:
        count_down(work_secs)
        label_top.configure(text="Work", fg=GREEN)

# ---------------------------- CLOCK ----------------------------
# TODO: add clock


def display_time():
    current_time = tm.strftime('%H:%M:%p')
    # canvas.itemconfig(clock_text, current_time)
    clock_label['text'] = current_time
    window.after(1000, display_time)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global my_timer

    mins = math.floor(count / 60)
    secs = count % 60
    if secs < 10:
        secs = f"0{secs}"

    canvas.itemconfig(timer_text, text=f'{mins}:{secs}')
    if count > 0:
        my_timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        mark = ""
        work_session = math.floor(reps / 2)
        for _ in range(work_session):
            mark += CHECKED
        label_bottom.config(text=mark)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro timer")
window.configure(padx=100, pady=50, bg=YELLOW)

# CANVAS AND IMAGE
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file='tomato.png')
canvas.create_image(100, 112, image=tomato_img)

# clock_text = canvas.create_text(65, 80, text="00:00", fill="white", font=(FONT_NAME, 16, "bold"))
# canvas.grid(row=2, column=2)

clock_label = Label(text="00:00", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 12, 'bold'))
clock_label.place(x=60, y=55)

timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=2, column=2)

label_top = Label(text='Timer', bg=YELLOW, fg=GREEN, font=(FONT_NAME, 35, 'bold'))
label_top.grid(row=1, column=2)

label_bottom = Label(bg=YELLOW, fg=GREEN, font=(FONT_NAME, 35, 'bold'))
label_bottom.grid(row=3, column=2)

button_start = Button(text='Start', highlightthickness=0, command=start_timer)
button_start.grid(row=3, column=1)

button_reset = Button(text='Reset', highlightthickness=0, command=reset_timer)
button_reset.grid(row=3, column=3)


# ---------------------------- EXTRAS ----------------------------
# TODO: log your study times divided by customizable materia.
# TODO: add dialog box
# TODO: add sound
# ---------------------------- Calls ----------------------------
display_time()

window.mainloop()