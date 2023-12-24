from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

current_card = {}

try:
    data = pandas.read_csv("../flash-card-app/data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("../flash-card-app/data/french_words.csv")

data_list = data.to_dict(orient="records")


def show_next_card():
    global current_card, timer
    window.after_cancel(timer)
    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(lang_text, text="French", fill="black")
    current_card = random.choice(data_list)
    next_word = current_card['French']
    canvas.itemconfig(word_text, text=next_word, fill="black")
    timer = window.after(3000, func=flip_card)


def is_known():
    global current_card, timer
    data_list.remove(current_card)
    to_learn = pandas.DataFrame(data_list)
    to_learn.to_csv("../flash-card-app/data/words_to_learn.csv", index=False)
    show_next_card()


def flip_card():
    global current_card
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(lang_text, text="English", fill="white")
    translation = current_card['English']
    canvas.itemconfig(word_text, text=translation, fill="white")


# -----------------------------------------------UI SETUP-----------------------------------------------#

window = Tk()
window.title("InstaCard Recall")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0)
card_front_img = PhotoImage(file="../flash-card-app/images/card_front.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
canvas.config(bg=BACKGROUND_COLOR)
lang_text = canvas.create_text(400, 150, text="French", fill="black", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", fill="black", font=("Arial", 60, "bold"))
canvas.grid(columnspan=2, column=0, row=0)

check_mark = PhotoImage(file="../flash-card-app/images/right.png")
known_button = Button(image=check_mark, padx=50, pady=50, highlightthickness=0, command=is_known)
known_button.grid(column=1, row=1)

cross_mark = PhotoImage(file="../flash-card-app/images/wrong.png")
unknown_button = Button(image=cross_mark, padx=50, pady=50, highlightthickness=0, command=show_next_card)
unknown_button.grid(column=0, row=1)

card_back_img = PhotoImage(file="../flash-card-app/images/card_back.png")

show_next_card()

window.mainloop()
