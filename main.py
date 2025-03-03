BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
import pandas
from random import choice

current_card={}
to_learn={}

try:
    data=pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data=pandas.read_csv("data/french_words.csv")
    to_learn=original_data.to_dict(orient="records")
else:    
    to_learn=data.to_dict(orient="records")


def next_card():
    global current_card,flip_timer
    window.after_cancel(flip_timer)
    current_card=choice(to_learn)
    french_word=current_card["French"]
    canvas.itemconfig(card_background, image=card_front)
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(word, text=french_word, fill="black")
    flip_timer=window.after(3000,flip_card)

def flip_card():
    canvas.itemconfig(language, text="English",fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background ,image=card_back)

def is_known():
    to_learn.remove(current_card)
    data=pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()    

window=Tk()
window.title("Flashy")
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)

flip_timer=window.after(3000, flip_card)

card_front=PhotoImage(file="images/card_front.png") 
card_back=PhotoImage(file="images/card_back.png")
canvas=Canvas(width=800,height=526)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_background=canvas.create_image(400,263,image=card_front)
canvas.grid(row=1,column=1, columnspan=2 )
language=canvas.create_text(400,150, text="", fill="black", font=("Arial",40, "italic"))
word=canvas.create_text(400,263, text="", fill="black", font=("Arial",60, "bold"))

cross_image=PhotoImage(file="images/wrong.png")
cross_button=Button(image=cross_image, highlightthickness=0,command=next_card)
cross_button.grid(row=2, column=1)

check_image=PhotoImage(file="images/right.png")
check_button=Button(image=check_image, highlightthickness=0, command=is_known)
check_button.grid(row=2, column=2)
next_card()

window.mainloop()