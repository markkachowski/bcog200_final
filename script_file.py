# I sort of lumped my outline for the project and description of functions into this file

import tkinter
import random
import os
from collections import (
    namedtuple,
    Counter,
)  ######################## see if theres another way of doing this

# root = tkinter.Tk()
# root.mainloop()

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
Card = namedtuple("Card", ["suit", "value"])

slappable_deck = []

player_deck = []
computer_deck = []

# 2 players
HAND_SIZE = 26

# is there another way to do this?
SUITS = ["♦️", "♥️", "♣️", "♠️"]
FACE_CARDS = ["J", "Q", "K", "A"]
FACE_CARD_VALUES = [11, 12, 13, 14]
POSSIBLE_NUMBERS_FOR_CARDS = list(range(2, 15, 1))
########################### NUMERIC_CARDS = [str(i) for i in POSSIBLE_NUMBERS_FOR_CARDS] since I need a GUI, face card values in the code can just be numbers 11-14, with 11 being a jack and 14 being an ace. or is this a bad idea
FACE_CARD_PLAY_VALUES = [1, 2, 3, 4]
# CHIP_VALUES = POSSIBLE_NUMBERS_FOR_CARDS + [11, 12, 13, 14] probably don't need


# function to create a deck,
########################## should the cards be indexed?
def create_deck():
    deck = [Card(suit, i) for suit in SUITS for i in POSSIBLE_NUMBERS_FOR_CARDS]
    return deck


# deck shuffling function
def shuffle_deck(deck):
    deck = random.shuffle(deck)
    return deck


# function to deal cards at the beginning of the game
def deal_hand(deck):
    start_deck_size = len(deck) // 2
    player_deck = deck[:start_deck_size]
    computer_deck = deck[start_deck_size:]

    print(
        f"Player deck:{player_deck, len(player_deck)}, Computer deck: {computer_deck, len(computer_deck)}"
    )  # check decks are equal and shuffled, get rid of this later you aren't allowed to look at your cards
    return player_deck, computer_deck


# Class for cards?
"figure out what to put here"


# class Card:
# what


# player turn function
"the turn that the user takes, check what the current card on the top of the deck is, then decide what to do."
"1. if top card is a face card, loop putting down cards until the correct number is reached, or the user puts down a face card"
"2. if out of cards then end the game"
"3. if it is just a numbered card, user places 1 card on the deck"


def player_turn(player_deck):
    ################## This is where things are gonna get funky, this function needs to have an input, (probably should be seperate from the slap input which I'm thinking should be spacebar), that allows you to put down a single card, UNLESS the previous card was a facecard
    ################## so not only does this function need to let the player put down one, or if necessary more than one card, it has to check if the last card was a face card
    ################## can you call a function inside of another function?, maybe I could have a seperate function checking if the last card placed was a face card
    ################## if worse comes to worse I could make it the bar version where face cards are like any other cards, except jacks are slappable
    pass


# computer turn function
"same as the player turn function, except that if the computer slaps, there will be a built in time delay from 0.2 seconds to 0.5 seconds"
"delay can change after testing it if its too easy or too hard"


# slap function/deck check function
"check the deck after each turn is taken to see if there is a slappable hand"
"when a slappable hand is detected, either the user or the computer can slap the deck"
"once deck is slapped, add all cards in play to the winners deck and wait for them to start the next hand"


def slap():
    ##################### This function needs to run so it can check if there is a slappable card after each card is put down, but will that make the game run slower? what is the optimal way to implement something like this
    # slap list needs to add the most recently played card, and check if there is a duplicate card value in the slappable_deck list
    # if not then do nothing, if there is, there has to be some sort of computer slap function, or maybe that could just be a aprt of this function, that lets the computer know it should slap the deck
    # There should either be a seperate deck for all cards in play, or the function that checks for a slappable hand needs to only look at the three most recent additions to the slappable deck
    # valid_slap = value[] in slappable_deck
    pass  # check if there is a duplicate number in the slappable deck. Since there should only be 3 cards in the slappable deck at any time, and slaps are sandwiches or doubles, if there are two of the same value, stop everything and anyone can slap


# false slap function
"if the player slaps when there is no valid slap, they lose one card, and that card goes to the bottom of the deck, and does not effect the active deck"

# face card function
"if a face card is detected at the top of the deck, the next player must put down the corresponding number of cards in a row, 1 for a jack 2 for a queen, 3 for a king, 4 for an ace"

# for card in entire_card_deck:
# pass

# class for computer?

# gui for the game
"needs to have at least 3 cards showing for the deck that is in play"
"probably would be nice to show more in case there is a face card where there would be up to 5 cards sort of active"
"maybe a number counter or other cards as a visual?"
"no need for a slap button but maybe could add one. slap should probably be a keyboard button"

# win/lose function(s)
"functions that end the game when the player either has all the cards, or runs out of all cards"
"check the number of cards currently in the player's deck"
"if the number of cards reaches 52, end the game and display a winning message"
"if the number of cards reaches 0, end the game, display a losing message"


# bonus things
"difficulties, easy normal or hard with quicker reaction times"
"sound effect for slapping maybe"


def main():
    deck = create_deck()

    shuffle_deck(deck)
    deal_hand(deck)
    player_turn(player_deck)


if __name__ == "__main__":
    main()

"""for i in range(NUM_HANDS):
        hand, deck = deal_hand(deck)
        report_info(hand, deck)"""
