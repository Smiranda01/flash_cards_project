from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"


class FlashCard(Tk):

    def __init__(self):
        super().__init__()
        self.current_card = {}
        self.to_learn = {}
        try:
            self.data = pandas.read_csv("words_to_learn.csv")
        except FileNotFoundError:
            self.original_data = pandas.read_csv("intermediate_words.csv")
            self.to_learn = self.original_data.to_dict("records")
        else:
            self.to_learn = self.data.to_dict("records")

        self.flip_timer = self.after(3000, self.flip_card)
        # Set up window
        self.title('Flashy')
        self.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
        # Set up Canvas and text inside
        self.canvas = Canvas(self, width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.card_front_img = PhotoImage(file="../images/card_front.png")
        self.card_back_img = PhotoImage(file="../images/card_back.png")
        self.canvas_image = self.canvas.create_image(400, 263, image=self.card_front_img)
        self.canvas.grid(column=0, row=0, columnspan=2)
        self.language_text = self.canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
        self.word_text = self.canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
        # Adding "right" button
        self.tick_image = PhotoImage(file="../images/right.png")
        self.known_button = Button(image=self.tick_image, borderwidth=0, highlightthickness=0,
                                   command=self.is_known)
        self.known_button.grid(column=1, row=1)
        # Adding "wrong" button
        self.cross_image = PhotoImage(file="../images/wrong.png")
        self.unknown_button = Button(image=self.cross_image, borderwidth=0, highlightthickness=0,
                                     command=self.is_not_known)
        self.unknown_button.grid(column=0, row=1)

        self.next_card()
        self.mainloop()

    def next_card(self):
        self.after_cancel(self.flip_timer)
        self.current_card = random.choice(self.to_learn)
        self.canvas.itemconfig(self.canvas_image, image=self.card_front_img)
        self.canvas.itemconfig(self.language_text, text="Español", fill="black")
        self.canvas.itemconfig(self.word_text, text=self.current_card["Spanish"], fill="black")
        self.after(3000, self.flip_card)

    def flip_card(self):
        self.canvas.itemconfig(self.canvas_image, image=self.card_back_img)
        self.canvas.itemconfig(self.language_text, text="English", fill="white")
        self.canvas.itemconfig(self.word_text, text=self.current_card["English"], fill="white")

    def is_known(self):
        self.to_learn.remove(self.current_card)
        data = pandas.DataFrame(self.to_learn)
        data.to_csv("words_to_learn.csv", index=False)
        self.next_card()

    def is_not_known(self):
        dont_know_list = [f"If you don't know '{self.current_card['Spanish']}' you have to study harder bro",
                          f"You should be studying for not knowing '{self.current_card['Spanish']}'",
                          f"You must review some lessons if you don't know '{self.current_card['Spanish']}'"]
        print(random.choice(dont_know_list))
        self.next_card()
