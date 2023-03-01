from tkinter import *
import pandas
import random
timer = None

BACKGROUND_COLOR = "#B1DDC6"
random_card = {}
to_learn = {}

try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("ru-eng.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

# ---------------------------- NEXT CARD ------------------------------- #
def next_card():
    global random_card, turn_timer
    window.after_cancel(turn_timer)
    random_card = random.choice(to_learn)
    canvas.itemconfig(lang, text="English", fill="black")
    canvas.itemconfig(current_word, text=random_card["English"], fill="black")
    canvas.itemconfig(canvas_image, image=card_front_image)
    turn_timer = window.after(3000, func=turn_card)


# ---------------------------- TURN CARD ------------------------------- #
def turn_card():
    canvas.itemconfig(canvas_image, image=card_back_image)
    canvas.itemconfig(lang, text="Russian", fill="white")
    canvas.itemconfig(current_word, text=random_card["Russian"], fill="white")


# ---------------------------- KNOWN CARD ------------------------------- #
def known_card():
    to_learn.remove(random_card)
    words_to_learn = pandas.DataFrame(to_learn)
    words_to_learn.to_csv("words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #

window =Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

turn_timer = window.after(3000, func=turn_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_image)
lang = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
current_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

wrong_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=wrong_img, highlightthickness=0, command=next_card)
unknown_button.grid(column=0, row=1)

right_img = PhotoImage(file="images/right.png")
known_button = Button(image=right_img, highlightthickness=0, command=known_card)
known_button.grid(column=1, row=1)






next_card()
window.mainloop()