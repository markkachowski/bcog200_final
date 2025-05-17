import time
import tkinter as tk
import random
import os
from tkinter import filedialog
from PIL import Image, ImageTk
from collections import (
    namedtuple,
    Counter,
)

Card = namedtuple("Card", ["suit", "value", "index"])


SUITS = ["♣️", "♦️", "♥️", "♠️"]
FACE_CARD_VALUES = [11, 12, 13, 14]
POSSIBLE_NUMBERS_FOR_CARDS = list(range(2, 15, 1))

deck = [
    Card(suit, value, index)
    for index, (value, suit) in enumerate(
        (value, suit) for value in POSSIBLE_NUMBERS_FOR_CARDS for suit in SUITS
    )
]


class GUI:
    def __init__(self, root):
        self.slaps = Game()
        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack()
        self.actions_label = tk.Label(
            root,
            text="#######Rules#######\nThe objective of Slaps is to get all 52 cards in the deck.\nYou are not allowed to see your cards. You can get cards by slapping when there are 2 of the\n same number card played in a row (eg. 2 of hearts and then a 2 of spades), or if a sandwich of 2 of\nthe same card occur (eg. king, queen, king). You can also slap when a jack is played.\nYou can slap at any time, but if there is not a valid slap, you will lose a card so be careful."
            "\nNormal difficulty is recommended if it is your first time playing or if you do not have a mouse.",
            font=("Ariel", 12, "bold"),
        )
        self.actions_label.pack(side="bottom", pady=50)

        self.normal_button = tk.Button(
            root,
            text="Normal",
            command=self.normal_difficulty,
            font=("Ariel", 14, "bold"),
            padx=10,
            pady=5,
        )
        self.normal_button.pack(side="left", padx=100)

        self.hard_button = tk.Button(
            root,
            text="Hard",
            fg="red",
            command=self.hard_difficulty,
            font=("Ariel", 14, "bold"),
            padx=10,
            pady=5,
        )
        self.hard_button.pack(side="left", padx=100)

        self.insane_button = tk.Button(
            root,
            text="INSANE",
            command=self.insane_difficulty,
            fg="black",
            bg="red",
            font=("Helvetica", 14, "bold", "italic"),
            padx=10,
            pady=5,
        )
        self.insane_button.pack(side="left", padx=100)
        self.displayed_cards = self.slaps.slappable_deck
        self.card_images = []

    def normal_difficulty(self):
        self.computer_slap_time = random.randint(900, 2000)
        self.computer_place_time = random.randint(550, 1100)
        self.button_size_x = 50
        self.button_size_y = 25
        self.button_font_size = 24
        self.normal_button.destroy()
        self.insane_button.destroy()
        self.hard_button.destroy()
        self.create_buttons()
        self.actions_label.config(text="Place a card to begin.")

    def hard_difficulty(self):
        self.computer_slap_time = random.randint(
            500, 850
        )  # probably need a mouse to beat this
        self.computer_place_time = random.randint(450, 900)
        self.button_size_x = 25
        self.button_size_y = 10
        self.button_font_size = 16
        self.hard_button.destroy()
        self.normal_button.destroy()
        self.insane_button.destroy()
        self.create_buttons()
        self.actions_label.config(text="Place a card to begin.")

    def insane_difficulty(self):
        self.computer_slap_time = random.randint(
            300, 550
        )  # barely within human reflex time, probably beatable on a touchscreen
        self.computer_place_time = random.randint(350, 700)
        self.button_size_x = 10
        self.button_size_y = 5
        self.button_font_size = 12
        self.insane_button.destroy()
        self.normal_button.destroy()
        self.hard_button.destroy()
        self.create_buttons()
        self.actions_label.config(text="Place a card to begin.")

    def create_buttons(self):

        place_card_button = tk.Button(
            root,
            text="Place Card",
            command=self.player_place_card,
            font=("Ariel", 12, "bold"),
            padx=25,
            pady=10,
        )
        place_card_button.pack(side="left", padx=200)

        self.slap_button = tk.Button(
            root,
            text="Slap",
            command=self.update_display_slap,
            font=("Ariel", self.button_font_size, "bold"),
            padx=self.button_size_x,
            pady=self.button_size_y,
        )

        self.slap_button.pack(side="right", padx=200)
        self.card_count_label = tk.Label(root, text="")
        self.card_count_label.pack(side="top")

    def player_place_card(self):
        if len(self.slaps.player_deck) == 0:
            self.actions_label.config(
                text=f"You Lost!\nYour average time to slap: {sum(self.slaps.slap_reaction_times) / len(self.slaps.slap_reaction_times)} seconds",
                font=("Ariel", 24, "bold"),
            )
        if self.slaps.player_move:
            self.slaps.player_turn()
            self.update_display_card_placed()
            for card in self.slaps.slappable_deck[-1]:
                self.placed_card_index = str(card)
            self.card_count_label.config(
                text=f"Your cards = {len(self.slaps.player_deck)}\nComputer cards = {len(self.slaps.computer_deck)}\nSlap pile cards = {len(self.slaps.slappable_deck)}"
            )
            self.actions_label.config(text="You placed a card.\nComputer's turn...")
            self.slaps.check_for_slap()
            if self.slaps.valid_slap:
                self.canvas.after(
                    self.computer_slap_time, self.update_display_computer_slap
                )
            elif self.slaps.valid_slap == False and self.slaps.player_move == False:
                self.canvas.after(self.computer_place_time, self.computer_place_card)

        elif not self.slaps.player_move and len(self.slaps.computer_deck) != 0:
            self.actions_label.config(text="It is not your turn.")

    def computer_place_card(self):
        if len(self.slaps.computer_deck) == 0:
            self.actions_label.config(
                text=f"You Won!\nYour average time to slap: {sum(self.slaps.slap_reaction_times) / len(self.slaps.slap_reaction_times)} seconds",
                font=("Ariel", 24, "bold"),
            )
        self.slaps.computer_turn()
        self.update_display_card_placed()
        for card in self.slaps.slappable_deck[-1]:
            self.placed_card_index = str(card)
        self.actions_label.config(text="Computer placed a card.\nIt is your turn...")
        self.card_count_label.config(
            text=f"Your cards = {len(self.slaps.player_deck)}\nComputer cards = {len(self.slaps.computer_deck)}\nSlap pile cards = {len(self.slaps.slappable_deck)}"
        )
        self.slaps.check_for_slap()
        if self.slaps.valid_slap:
            self.canvas.after(
                self.computer_slap_time, self.update_display_computer_slap
            )

    def update_display_card_placed(
        self,
    ):
        self.canvas.delete("all")
        self.card_images.clear()

        for i, card in enumerate(self.displayed_cards[-3:]):
            self.path = f"images/{card.index + 1}.png"
            if os.path.exists(self.path):
                self.image_file = Image.open(self.path).resize((125, 185))
                self.card_picture = ImageTk.PhotoImage(self.image_file)
                self.card_images.append(self.card_picture)
                self.canvas.create_image(160 * i + 150, 100, image=self.card_picture)

    def update_display_slap(self):
        if self.slaps.valid_slap == True:
            self.slaps.slap()
            self.canvas.delete("all")
            self.displayed_cards.clear()
            self.actions_label.config(
                text="You slapped!\nSince you won the last hand it is now your turn."
            )
            self.card_count_label.config(
                text=f"Your cards = {len(self.slaps.player_deck)}\nComputer cards = {len(self.slaps.computer_deck)}\nSlap pile cards = {len(self.slaps.slappable_deck)}"
            )
        elif self.slaps.valid_slap == False:
            self.slaps.slap()
            self.actions_label.config(text="False slap, -1 Card!")
            self.card_count_label.config(
                text=f"Your cards = {len(self.slaps.player_deck)}\nComputer cards = {len(self.slaps.computer_deck)}\nSlap pile cards = {len(self.slaps.slappable_deck)}"
            )

    def update_display_computer_slap(self):
        if self.slaps.valid_slap == True:
            self.slaps.computer_slap()
            self.canvas.delete("all")
            self.displayed_cards.clear()
            self.actions_label.config(text="Computer Slapped!\nSince you lost the hand it is now the computer's turn...")
            self.computer_slap_recover_time = random.randint(1700, 2400)
            self.canvas.after(self.computer_slap_recover_time, self.computer_place_card)
            self.card_count_label.config(
                text=f"Your cards = {len(self.slaps.player_deck)}\nComputer cards = {len(self.slaps.computer_deck)}\nSlap pile cards = {len(self.slaps.slappable_deck)}"
            )


class Game:
    def __init__(self):

        self.deck = [
            Card(suit, value, index)
            for index, (value, suit) in enumerate(
                (value, suit) for value in POSSIBLE_NUMBERS_FOR_CARDS for suit in SUITS
            )
        ]
        random.shuffle(self.deck)
        self.start_deck_size = len(self.deck) // 2
        self.player_deck = self.deck[: self.start_deck_size]
        self.computer_deck = self.deck[self.start_deck_size :]
        self.slappable_deck = []
        self.valid_slap = False
        self.player_move = True
        self.computer_move = False
        self.slap_reaction_times = []

    def check_for_slap(self):
        self.slap_pattern_trio = []
        self.last_three_cards = self.slappable_deck[-3:]
        self.most_recent_card = self.slappable_deck[-1]
        for card in self.last_three_cards:
            self.slap_pattern_trio.append(card.value)
        if len(self.slap_pattern_trio) != len(set(self.slap_pattern_trio)):
            self.valid_slap_start_time = time.time()
            self.valid_slap = True
            self.computer_slapped = False
            self.player_slapped = False
        elif self.most_recent_card.value == FACE_CARD_VALUES[0]:
            self.valid_slap_start_time = time.time()
            self.valid_slap = True
            self.computer_slapped = False
            self.player_slapped = False

    def player_turn(self):
        if self.player_move:
            self.removed_player_card = self.player_deck.pop()
            self.slappable_deck.append(self.removed_player_card)
            self.player_move = False
            self.computer_move = True
            self.player_slapped = False
            self.computer_slapped = False

    def computer_turn(self):
        if not self.player_move:
            self.removed_computer_card = self.computer_deck.pop()
            self.slappable_deck.append(self.removed_computer_card)
            self.player_move = True
            self.computer_move = False

    def slap(self):
        if self.valid_slap == True and self.computer_slapped == False:
            self.time_taken_for_slap = time.time()
            self.reaction_time = self.time_taken_for_slap - self.valid_slap_start_time
            self.slap_reaction_times.append(self.reaction_time)
            while not self.computer_slapped and not self.player_slapped:
                for card in self.slappable_deck:
                    self.player_deck.insert(0, card)
                self.slappable_deck.clear()
                self.player_slapped = True
                self.player_move = True
                self.computer_move = False
                self.valid_slap = False

        elif self.valid_slap == False:
            self.removed_player_card = self.player_deck.pop()
            self.slappable_deck.insert(0, self.removed_player_card)
            self.valid_slap = False

    def computer_slap(self):
        if self.valid_slap and not self.player_slapped:
            for card in self.slappable_deck:
                self.computer_deck.insert(0, card)
            self.slappable_deck.clear()
            self.player_move = False
            self.computer_move = True
            self.valid_slap = False
            self.computer_slapped = True


if __name__ == "__main__":
    root = tk.Tk()
    slaps = GUI(root)
    root.mainloop()
