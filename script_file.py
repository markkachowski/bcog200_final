# I sort of lumped my outline for the project and description of functions into this file

import tkinter
import random
import os
from collections import namedtuple, Counter # see if theres another way of doing this

root = tkinter.Tk()
root.mainloop()

# for the "slappable deck", you only need 3 cards at any given time
# have them in a list?
# use something else?
# gui for cards in slappable deck
# suit does not matter very much for the game but it should still be included
# card bank for player and computer

# Define global things
"how many cards need to be put down for a face card? Or could this go in the face card function"
"number of cards in the deck"


# Card constants mostly the same from the card_demo, see if there is another weay of doing this
Card = namedtuple("Card", ["suit", "value"])
Hand = namedtuple("Hand", ["cards"])


#2 players
HAND_SIZE = 26

# is there another way to do this?
SUITS = ["♦️", "♥️", "♣️", "♠️"]
FACE_CARDS = ["J", "Q", "K", "A"]
FACE_CARD_VALUES = [11, 12, 13, 14]
POSSIBLE_NUMBERS_FOR_CARDS = list(range(2, 11, 1))
NUMERIC_CARDS = [str(i) for i in POSSIBLE_NUMBERS_FOR_CARDS]
FACE_CARD_PLAY_VALUES = [1, 2, 3, 4]
CHIP_VALUES = POSSIBLE_NUMBERS_FOR_CARDS + [11, 12, 13, 14]


#function to create a deck
def create_deck():
    deck = [
        Card(suit, CHIP_VALUES)
        for suit in SUITS
    ]
    return deck




# deck shuffling function
def shuffle_deck(deck):
    random.shuffle(deck)
    return deck

def deal_hand(deck, hand_size=HAND_SIZE):
    half_deck = deck[hand_size]


    player_hand = Hand(
        cards=half_deck)

    computer_hand = Hand(
        cards=half_deck)
    print(player_hand)
    return player_hand, computer_hand


slappable_deck = ()

player_deck = ()
computer_deck = ()

# Class for cards?
"figure out what to put here"
class Card:
    what

# player turn function
"the turn that the user takes, check what the current card on the top of the deck is, then decide what to do."
"1. if top card is a face card, loop putting down cards until the correct number is reached, or the user puts down a face card"
"2. if out of cards then end the game"
"3. if it is just a numbered card, user places 1 card on the deck"
def player_turn():
    if 


# computer turn function
"same as the player turn function, except that if the computer slaps, there will be a built in time delay from 0.2 seconds to 0.5 seconds"
"delay can change after running it maybe thats too easy"


# slap function/deck check function
"check the deck after each turn is taken to see if there is a slappable hand"
"when a slappable hand is detected, either the user or the computer can slap the deck"
"once deck is slapped, add all cards in play to the winners deck and wait for them to start the next hand"
def slap():
    valid_slap = value[] in slappable_deck #check if there is a duplicate number in the slappable deck. Since there should only be 3 cards in the slappable deck at any time, and slaps are sandwiches or doubles, if there are two of the same value, stop everything and anyone can slap

#false slap function
"if the player slaps when there is no valid slap, they lose one card, and that card goes to the bottom of the deck, and does not effect the active deck"

# face card function
"if a face card is detected at the top of the deck, the next player must put down the corresponding number of cards in a row, 1 for a jack 2 for a queen, 3 for a king, 4 for an ace"

for card in entire_card_deck:
    if card 

# class for computer?

#gui for the game
"needs to have at least 3 cards showing for the deck that is in play"
"probably would be nice to show more in case there is a face card where there would be up to 5 cards sort of active"
"maybe a number counter or other cards as a visual?"
"no need for a slap button but maybe could add one. slap should probably be a keyboard button"

#win/lose function(s)
"functions that end the game when the player either has all the cards, or runs out of all cards"
"check the number of cards currently in the player's deck"
"if the number of cards reaches 52, end the game and display a winning message"
"if the number of cards reaches 0, end the game, display a losing message"


# bonus things
"difficulties, easy normal or hard with quicker reaction times"
"sound effect for slapping maybe"


def main():
    deck = create_deck()

    deck = shuffle_deck(deck)
    for i in range(NUM_HANDS):
        hand, deck = deal_hand(deck)
        report_info(hand, deck)


if __name__ == "__main__":
    main()
