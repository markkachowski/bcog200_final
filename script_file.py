# I sort of lumped my outline for the project and description of functions into this file


import time
import tkinter as tk
import random
import os
from tkinter import filedialog
from PIL import Image, ImageTk
from collections import (
    namedtuple,
    Counter,
)  ######################## see if theres another way of doing this


# for the "slappable deck", you only need 3 cards at any given time
##################### have them in a list?
###################### use something else?
# gui for cards in slappable deck
# suit does not matter very much for the game but it should still be included
# card bank for player and computer

"Define global things"
########################"how many cards need to be put down for a face card? Or could this go in the face card function"
"number of cards in the deck"


################################### Card constants mostly the same from the card_demo, see if there is another weay of doing this
Card = namedtuple("Card", ["suit", "value", "index"])

# figure out a way to keep track of whose turn it is

SUITS = ["♣️", "♦️", "♥️", "♠️"]
FACE_CARDS = ["J", "Q", "K", "A"]
FACE_CARD_VALUES = [11, 12, 13, 14]
POSSIBLE_NUMBERS_FOR_CARDS = list(range(2, 15, 1))
FACE_CARD_PLAY_VALUES = [1, 2, 3, 4]

# Error time

# cards are being appended somewhere else or deleted, and not being added to the player and computer decks after a slap

deck = [
    Card(suit, value, index)
    for index, (value, suit) in enumerate(
        (value, suit) for value in POSSIBLE_NUMBERS_FOR_CARDS for suit in SUITS
    )
]


class GUI:
    def __init__(self, root):
        self.slaps = Game()
        self.canvas = tk.Canvas(
            root, width=600, height=400
        )  # change if this is a weird size
        self.canvas.pack()
        # add instructions at the start
        self.actions_label = tk.Label(root, text="")
        self.actions_label.pack(side="bottom", pady=50)  # Change

        # To make sure the card being put down is actually the card displayed, delete later
        self.card_label = tk.Label(root, text="")
        self.card_label.pack(side="bottom", pady=150)

        self.player_card_count_label = tk.Label(root, text="")
        self.player_card_count_label.pack(side="top", padx=100)

        place_card_button = tk.Button(
            root, text="Place Card", command=self.player_place_card
        )
        place_card_button.pack(side="left", padx=100)  # make bigger?

        slap_button = tk.Button(root, text="Slap", command=self.update_display_slap)
        slap_button.pack(side="right", padx=100)  # make bigger later
        self.displayed_cards = self.slaps.slappable_deck
        self.card_images = []

    # def display_card_values(self):

    def player_place_card(self):
        if self.slaps.player_move:
            self.slaps.player_turn()
            self.update_display_card_placed()
            for card in self.slaps.slappable_deck[-1]:
                self.placed_card_index = str(card)
            self.card_label.config(text=self.placed_card_index)
            self.player_card_count_label.config(
                text=f"Your cards = {len(self.slaps.player_deck)}"
            )
            self.actions_label.config(text="You placed a card.")
            self.slaps.check_for_slap()
            if self.slaps.valid_slap == False and self.slaps.player_move == False:
                self.computer_place_time = random.randint(700, 1200)
                self.canvas.after(self.computer_place_time, self.computer_place_card)
            elif self.slaps.valid_slap:
                self.computer_slap_time = random.randint(1700, 2400)
                self.canvas.after(
                    self.computer_slap_time, self.update_display_computer_slap
                )
        elif not self.slaps.player_move:
            self.actions_label.config(text="It is not your turn.")

    def computer_place_card(self):
        self.slaps.computer_turn()
        self.update_display_card_placed()
        for card in self.slaps.slappable_deck[-1]:
            self.placed_card_index = str(card)
        self.card_label.config(text=self.placed_card_index)
        self.actions_label.config(text="Computer placed a card.")
        self.slaps.check_for_slap()
        if self.slaps.valid_slap:
            self.computer_slap_time = random.randint(1700, 2400)
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
                self.image_file = Image.open(self.path).resize(
                    (100, 150)
                )  # change if this is a weird size
                self.card_picture = ImageTk.PhotoImage(self.image_file)
                self.card_images.append(self.card_picture)
                self.canvas.create_image(
                    120 * i + 50, 100, image=self.card_picture
                )  # get this to overlap later # change if this is a weird size

    def update_display_slap(self):
        if self.slaps.valid_slap == True:
            self.slaps.slap()
            self.canvas.delete("all")
            self.displayed_cards.clear()
            self.actions_label.config(text="Yeehaw, you slapped!")
        elif self.slaps.valid_slap == False:
            self.slaps.slap()
            self.actions_label.config(text="False slap, -1 Card!")

    def update_display_computer_slap(self):
        if self.slaps.valid_slap == True:
            self.slaps.computer_slap()
            self.canvas.delete("all")
            self.displayed_cards.clear()
            self.actions_label.config(text="Computer Slapped!")
            self.computer_slap_recover_time = random.randint(1700, 2400)
            self.canvas.after(self.computer_slap_recover_time, self.computer_place_card)


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

    def player_turn(self):
        if self.player_move:
            self.removed_player_card = self.player_deck.pop()
            self.slappable_deck.append(self.removed_player_card)
            self.player_move = False
            self.player_slapped = False
            self.computer_slapped = False

    def computer_turn(self):
        if not self.player_move:
            self.removed_computer_card = self.computer_deck.pop()
            self.slappable_deck.append(self.removed_computer_card)
            self.player_move = True
            self.player_slapped = False
            self.computer_slapped = False

    def check_face_card(self):  # this might need to be changed to just jacks
        if len(self.slappable_deck) != 0:
            self.most_recent_card = self.slappable_deck[-1]
            self.face_card_list = []
            if self.most_recent_card.value in FACE_CARD_VALUES:
                self.is_face_card = True
            else:
                self.is_face_card = False
        else:
            pass

    def check_for_slap(self):
        self.slap_pattern_trio = []
        self.last_three_cards = self.slappable_deck[-3:]
        for card in self.last_three_cards:
            self.slap_pattern_trio.append(card.value)
        if len(self.slap_pattern_trio) != len(set(self.slap_pattern_trio)):
            self.valid_slap = True
            self.computer_slapped = False
            self.player_slapped = False

    def slap(self):
        if self.valid_slap == True and self.computer_slapped == False:
            while not self.computer_slapped and not self.player_slapped:
                for card in self.slappable_deck:
                    self.player_deck.insert(0, card)
                self.slappable_deck.clear()
                self.player_slapped = True
                self.player_move = True
                self.valid_slap = False
        if self.valid_slap == False:
            self.removed_player_card = self.player_deck.pop()
            self.slappable_deck.insert(0, self.removed_player_card)
            self.valid_slap = False

    def computer_slap(self):
        if self.valid_slap and not self.player_slapped:
            for card in self.slappable_deck:
                self.computer_deck.insert(0, card)
                self.slappable_deck.clear()
            self.player_move = False
            self.valid_slap = False
            self.computer_slapped = True

    def gameplay_loopithink(self):
        while len(self.player_deck) != 0 and len(self.computer_deck) != 0:
            self.check_for_slap()
            self.is_face_card = self.check_face_card()
            self.player_turn()
            self.check_for_slap()
            self.is_face_card = self.check_face_card()
            self.computer_turn()
        if len(self.computer_deck) == 0:
            self.actions_label.config(text="You won!")
        elif len(self.player_deck) == 0:
            self.actions_label.config(text="You lost!")


if __name__ == "__main__":
    root = tk.Tk()
    slaps = GUI(root)
    root.mainloop()


# player turn function
"the turn that the user takes, check what the current card on the top of the deck is, then decide what to do."
"1. if top card is a face card, loop putting down cards until the correct number is reached, or the user puts down a face card"
"2. if out of cards then end the game"
"3. if it is just a numbered card, user places 1 card on the deck"


# computer turn function
"same as the player turn function, except that if the computer slaps, there will be a built in time delay from 0.2 seconds to 0.5 seconds"
"delay can change after testing it if its too easy or too hard"
# Probably don't even need this anymore
# else: #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
# print("Computer slapped!")
# for card in self.slappable_deck:
#   self.computer_deck.insert(0, card)
# self.slappable_deck.clear()

# slap function/deck check function (This and the slap function could possibly be combined into one for the purposes of testing, and then once the GUI is developed it can go back to being seperate)
"check the deck after each turn is taken to see if there is a slappable hand"
"when a slappable hand is detected, either the user or the computer can slap the deck"
"once deck is slapped, add all cards in play to the winners deck and wait for them to start the next hand"

"""def main():
    deck = create_deck()

    shuffle_deck(deck)
    deal_hand(deck)
    player_deck, computer_deck = deal_hand(deck)
    while len(player_deck) != 0 and len(computer_deck) != 0:
        slap(player_deck, computer_deck, slappable_deck)
        is_face_card = check_face_card(slappable_deck)
        player_turn(player_deck, slappable_deck, is_face_card)
        slap(player_deck, computer_deck, slappable_deck)
        is_face_card = check_face_card(slappable_deck)
        computer_turn(computer_deck, slappable_deck, is_face_card)
    if len(computer_deck) == 0:
        print("You won!")
    else:
        print("You lost!")


if __name__ == "__main__":
    main()


# Face card checking code, maybe will be its own function"""

"""

# All these need to take the turn as normal unless another face card is put down, in which case it then goes to the computers turn
def check_face_card(slappable_deck):
    for card in slappable_deck[-1]:
        if card.value == 11:
            for value in FACE_CARD_PLAY_VALUES[0]:
                print("Jack detected")
                continue
        elif card.value == 12:
            for value in FACE_CARD_PLAY_VALUES[
                1
            ]:  # make a new temporary list, put the cards in both, loop the input for putting down cards until the list length equals FACE_CARD_PLAY_VALUES[i]?
                print(
                    "Queen detected"
                )  # if another face card is put down, clear or detroy the temporary list and make a new one, and also make it the next person's turn
                continue
        elif card.value == 13:
            for value in FACE_CARD_PLAY_VALUES[2]:
                print("King detected")
                continue
        elif card.value == 14:
            for value in FACE_CARD_PLAY_VALUES[3]:
                print("Ace detected")
                continue
        else:
            print(
                "take turn as normal: put down one card, check for a slap, and then go to the computer"
            )"""

"""
def create_the_gui(root):
    root.title("Slaps")

    # GUI setup
    canvas = tk.Canvas(root, width=600, height=400)
    canvas.pack()

    place_card_button = tk.Button(root, text="Place Card", command=place_card)
    place_card_button.pack(side="left", padx=100)

    slap_button = tk.Button(root, text="Slap", command=slap)
    slap_button.pack(side="right", padx=100)
    displayed_cards = []"""
