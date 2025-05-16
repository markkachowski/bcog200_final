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


SUITS = ["♣️", "♦️", "♥️", "♠️"]
FACE_CARDS = ["J", "Q", "K", "A"]
FACE_CARD_VALUES = [11, 12, 13, 14]
POSSIBLE_NUMBERS_FOR_CARDS = list(range(2, 15, 1))
FACE_CARD_PLAY_VALUES = [1, 2, 3, 4]

# Error time

# computer put down 5 cards for an ace instead of 4 and despite winning i didnt win
# logic for me placing a jack was right but the display updated too quick
# winning with face cards doesn't update the screen
# computer doesn't slap when double jacks are placed

######### Go through and fix all the logic


# things to add
# win/lose messages
# make gui look nice
# player fc functionality
# weird things that don't quite work right
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
        self.actions_label = tk.Label(
            root,
            text="#######Rules#######\nThe objective of Slaps is to get all the cards in the deck.\nYou can get cards by slapping anytime 2 of\n the same number card are played in a row, or if a sandwich of 2 of\nthe same card occur. You can sometimes win by placing a face card as well. When you place a\nface card, the next player has a certain number of chances to place a face card as well:\n1 card for a jack, 2 for a queen, 3 for king, 4 for ace. If the player does not place a face card,\nthen you win the hand. If they do place one, then you must put down the corresponding number of cards\nand hope for a face card or a slap, otherwise you will lose that hand. You can slap at any time, but if\n there is not a valid slap, you will lose a card so be careful before you slap.",
            font=("Ariel", 11, "bold"),
        )
        self.actions_label.pack(side="bottom", pady=50)  # Change

        # To make sure the card being put down is actually the card displayed, delete later
        # self.card_label = tk.Label(
        #    root,
        # )
        # self.card_label.pack(side="bottom", pady=150)

        self.card_count_label = tk.Label(root, text="")
        self.card_count_label.pack(side="top")

        place_card_button = tk.Button(
            root,
            text="Place Card",
            command=self.player_place_card,
            font=("Ariel", 16, "bold"),
            padx=25,
            pady=10,
        )
        place_card_button.pack(side="left", padx=200)  # make bigger?

        slap_button = tk.Button(
            root,
            text="Slap",
            command=self.update_display_slap,
            font=("Ariel", 16, "bold"),
            padx=25,
            pady=10,
        )
        slap_button.pack(side="right", padx=200)  # make bigger later
        self.displayed_cards = self.slaps.slappable_deck
        self.card_images = []

    # def display_card_values(self):

    def player_place_card(self):
        if self.slaps.player_move:
            self.slaps.player_turn()
            self.update_display_card_placed()
            for card in self.slaps.slappable_deck[-1]:
                self.placed_card_index = str(card)
            # self.card_label.config(text=self.placed_card_index)
            self.card_count_label.config(
                text=f"Your cards = {len(self.slaps.player_deck)}\nComputer cards = {len(self.slaps.computer_deck)}\nSlap pile cards = {len(self.slaps.slappable_deck)}"
            )
            self.actions_label.config(text="You placed a card.")
            self.slaps.check_for_slap()
            if self.slaps.valid_slap:
                self.computer_slap_time = random.randint(700, 1100)
                self.canvas.after(
                    self.computer_slap_time, self.update_display_computer_slap
                )
            elif self.slaps.valid_slap == False and self.slaps.player_move == False:
                self.computer_place_time = random.randint(550, 1100)
                self.canvas.after(self.computer_place_time, self.computer_place_card)

        # elif self.slaps.player_move and self.slaps.player_fc_move:
        elif not self.slaps.player_move:
            self.actions_label.config(text="It is not your turn.")

    # def player_fc_move(self):

    def computer_place_card(self):
        self.slaps.computer_turn()
        self.update_display_card_placed()
        # if self.slaps.is_face_card:
        #    self.computer_turn_fc()
        #    self.update_display_card_placed()
        for card in self.slaps.slappable_deck[-1]:
            self.placed_card_index = str(card)
        # self.card_label.config(text=self.placed_card_index)
        self.actions_label.config(text="Computer placed a card.")
        self.card_count_label.config(
            text=f"Your cards = {len(self.slaps.player_deck)}\nComputer cards = {len(self.slaps.computer_deck)}\nSlap pile cards = {len(self.slaps.slappable_deck)}"
        )
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
                    120 * i + 150, 100, image=self.card_picture
                )  # get this to overlap later # change if this is a weird size

    def update_display_slap(self):
        self.slaps.check_for_slap()
        if self.slaps.valid_slap == True:
            self.slaps.slap()
            self.canvas.delete("all")
            self.displayed_cards.clear()
            self.actions_label.config(
                text="You slapped!\nSince you won the last hand it is now your turn."
            )
            self.card_count_label.config(
                text=f"Your cards = {len(self.slaps.player_deck)}\nComputer cards = {len(self.slaps.computer_deck)}\nSlap pile cards = {len(self.slaps.slappable_deck)}\nmost recent card = {self.slaps.player_deck[0]}"
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
            self.actions_label.config(text="Computer Slapped!")
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

    def check_for_slap(self):
        self.slap_pattern_trio = []
        self.last_three_cards = self.slappable_deck[-3:]
        self.most_recent_card = self.slappable_deck[-1]
        for card in self.last_three_cards:
            self.slap_pattern_trio.append(card.value)
        if len(self.slap_pattern_trio) != len(set(self.slap_pattern_trio)):
            self.valid_slap = True
            self.computer_slapped = False
            self.player_slapped = False
        elif self.most_recent_card.value == FACE_CARD_VALUES[0]:
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

    def gameplay_loopithink(self):
        while len(self.player_deck) != 0 and len(self.computer_deck) != 0:
            self.check_for_slap()
            self.player_turn()
            self.check_for_slap()
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

"""    def end_computer_turn(self):
        self.slaps.check_for_slap()
        self.canvas.after(self.comp_card_delay, self.update_display_card_placed())
        self.card_count_label.config(
            text=f"Your cards = {len(self.slaps.player_deck)}\nComputer cards = {len(self.slaps.computer_deck)}\nSlap pile cards = {len(self.slaps.slappable_deck)}"
        )
        self.slaps.computer_move = False
        self.slaps.player_move = True
        self.update_display_card_placed()
        self.actions_label.config(text=f"You won this hand with face cards!")

    def computer_turn_fc(self, step=0):
        self.computer_slap_time_when_fcs = random.randint(1100, 1500)
        self.slaps.check_for_slap()
        if not self.slaps.computer_move:
            return
        if self.slaps.valid_slap:
            self.canvas.after(
                self.computer_slap_time_when_fcs, self.update_display_computer_slap()
            )
        elif not self.slaps.valid_slap:
            if self.slaps.is_jack_rule:
                self.slaps.comp_clean_fc_final()
                self.update_display_card_placed()
                self.canvas.after(
                    self.comp_card_delay, lambda: self.end_computer_turn()
                )

            elif self.slaps.is_queen_rule and step < 2:
                self.slaps.comp_fc_clean_loop()
                self.update_display_card_placed()
                self.canvas.after(
                    self.comp_card_delay, lambda: self.computer_turn_fc(step + 1)
                )
            elif self.slaps.is_queen_rule and step == 2:
                self.slaps.comp_clean_fc_final()
                self.update_display_card_placed()
                self.canvas.after(
                    self.comp_card_delay, lambda: self.end_computer_turn()
                )

            elif self.slaps.is_king_rule and step < 3:
                self.slaps.comp_fc_clean_loop()
                self.update_display_card_placed()
                self.canvas.after(
                    self.comp_card_delay, lambda: self.computer_turn_fc(step + 1)
                )
            elif self.slaps.is_king_rule and step == 3:
                self.slaps.comp_clean_fc_final()
                self.update_display_card_placed()
                self.canvas.after(
                    self.comp_card_delay, lambda: self.end_computer_turn()
                )

            elif self.slaps.is_ace_rule and step < 4:
                self.slaps.comp_fc_clean_loop()
                self.update_display_card_placed()
                self.canvas.after(
                    self.comp_card_delay, lambda: self.computer_turn_fc(step + 1)
                )
            elif self.slaps.is_ace_rule and step == 4:
                self.slaps.comp_clean_fc_final()
                self.update_display_card_placed()
                self.canvas.after(
                    self.comp_card_delay, lambda: self.end_computer_turn()
                )
                
                    def comp_fc_clean_loop(self):
        # self.is_face_card = False
        if self.computer_deck:
            self.removed_computer_card = self.computer_deck.pop()
            self.slappable_deck.append(self.removed_computer_card)
        else:
            self.computer_lost = True
        self.check_face_card()
        if self.is_face_card:
            self.computer_move = False
            self.player_move = True
            self.player_fc_move = True
            self.computer_move = False  # these might need to be changed when fc rules are implemented for the player
            self.is_jack_rule = False
            self.is_queen_rule = False
            self.is_king_rule = False
            self.is_ace_rule = False
            # self.check_face_card_type()
        else:
            pass

    def comp_clean_fc_final(self):
        if self.computer_move:
            # self.is_face_card = False
            if self.computer_deck:
                self.removed_computer_card = self.computer_deck.pop()
                self.slappable_deck.append(self.removed_computer_card)
            else:
                self.computer_lost = True
            self.check_face_card()
            if self.is_face_card:
                self.computer_move = False
                self.player_move = True
                self.player_fc_move = True
                self.check_face_card_type()
            elif not self.is_face_card:
                for card in self.slappable_deck:
                    self.player_deck.insert(0, card)
                self.slappable_deck.clear()
                self.player_move = True
                self.is_jack_rule = False
                self.is_queen_rule = False
                self.is_king_rule = False
                self.is_ace_rule = False
                
                    def check_face_card(self):
        self.most_recent_card = self.slappable_deck[-1]
        if self.most_recent_card.value in FACE_CARD_VALUES:
            self.is_face_card = True
            if self.most_recent_card.value == 11:
                self.is_jack_rule = True
            elif self.most_recent_card.value == 12:
                self.is_queen_rule = True
            elif self.most_recent_card.value == 13:
                self.is_king_rule = True
            elif self.most_recent_card.value == 14:
                self.is_ace_rule = True
        else:
            self.is_face_card = False

    def check_face_card_type(self):
        # should an if statement be here?
        if self.most_recent_card.value == 11:
            self.is_jack_rule = True
        elif self.most_recent_card.value == 12:
            self.is_queen_rule = True
        elif self.most_recent_card.value == 13:
            self.is_king_rule = True
        elif self.most_recent_card.value == 14:
            self.is_ace_rule = True"""
