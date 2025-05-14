"A user can test my file by running the program, and seeing if the game functions as intended. This means that it is fair (computer isn't super good or super bad), it can't be exploited, it works as intended,"

# I sort of lumped my outline for the project and description of functions into this file

import time
import tkinter as tk
import random
import os
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
Card = namedtuple("Card", ["suit", "value"])

slappable_deck = []
SUITS = ["♣️", "♦️", "♥️", "♠️"]
FACE_CARDS = ["J", "Q", "K", "A"]
FACE_CARD_VALUES = [11, 12, 13, 14]
POSSIBLE_NUMBERS_FOR_CARDS = list(range(2, 15, 1))
########################### NUMERIC_CARDS = [str(i) for i in POSSIBLE_NUMBERS_FOR_CARDS] since I need a GUI, face card values in the code can just be numbers 11-14, with 11 being a jack and 14 being an ace. or is this a bad idea
FACE_CARD_PLAY_VALUES = [1, 2, 3, 4]
# CHIP_VALUES = POSSIBLE_NUMBERS_FOR_CARDS + [11, 12, 13, 14] probably don't need


# function to create a deck,
# cards should probably be indexed
def create_deck():
    # deck = [Card(suit, i) for i in POSSIBLE_NUMBERS_FOR_CARDS for suit in SUITS]
    # print(deck)
    deck = [Card(suit, i) for i in POSSIBLE_NUMBERS_FOR_CARDS for suit in SUITS]
    deck = {card: i + 1 for i, card in enumerate(deck)}

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

    # print(f"Player deck:{player_deck, len(player_deck)} \n Computer deck: {computer_deck, len(computer_deck)}")
    return player_deck, computer_deck


# player turn function
"the turn that the user takes, check what the current card on the top of the deck is, then decide what to do."
"1. if top card is a face card, loop putting down cards until the correct number is reached, or the user puts down a face card"
"2. if out of cards then end the game"
"3. if it is just a numbered card, user places 1 card on the deck"


def player_turn(player_deck, slappable_deck, is_face_card):
    ################## This is where things are gonna get funky, this function needs to have an input (will be a button), that allows you to put down a single card, UNLESS the previous card was a facecard
    ################## so not only does this function need to let the player put down one, or if necessary more than one card, it has to check if the last card was a face card
    ################## needs to check card value after each card is placed to see if it is a face card, in case you place one while already putting down multiple for the computer's face card
    ################## if worse comes to worse I could make it the bar version where face cards are like any other cards, except jacks are slappable
    # card_debt_value = FACE_CARD_VALUES - 10
    # there is definitely a better way to do this
    ################### should placing a card be its own function?

    place_card = input("")
    if is_face_card:
        cards_for_fc = []

        print("face card detected")
    if place_card == "":
        print("yeehaw you placed a card")
        removed_player_card = player_deck.pop()
        slappable_deck.append(removed_player_card)

    for card in slappable_deck[-5:]:
        print(card)
    return player_deck, slappable_deck


# computer turn function
"same as the player turn function, except that if the computer slaps, there will be a built in time delay from 0.2 seconds to 0.5 seconds"
"delay can change after testing it if its too easy or too hard"


def computer_turn(computer_deck, slappable_deck, is_face_card):

    # computer_reaction_time = random.uniform(0.25, 0.5)
    # time.sleep(computer_reaction_time)
    if is_face_card:
        print("face card detected")
    removed_computer_card = computer_deck.pop()
    slappable_deck.append(removed_computer_card)
    print("\nComputer placed a card")
    for card in slappable_deck[-5:]:
        print(card)
    return computer_deck, slappable_deck


# slap function/deck check function (This and the slap function could possibly be combined into one for the purposes of testing, and then once the GUI is developed it can go back to being seperate)
"check the deck after each turn is taken to see if there is a slappable hand"
"when a slappable hand is detected, either the user or the computer can slap the deck"
"once deck is slapped, add all cards in play to the winners deck and wait for them to start the next hand"


def check_for_slap(slappable_deck):
    slap_pattern_trio = []
    last_three_cards = slappable_deck[-3:]
    for card in last_three_cards:
        slap_pattern_trio.append(card.value)
    if len(slap_pattern_trio) != len(set(slap_pattern_trio)):
        print("slap detected")
        valid_slap = True
        return slappable_deck, valid_slap
    else:
        valid_slap = False
        return valid_slap


# Face Card checking function
def check_face_card(slappable_deck):
    if len(slappable_deck) != 0:
        most_recent_card = slappable_deck[-1]
        face_card_list = []
        if most_recent_card.value in FACE_CARD_VALUES:
            is_face_card = True
            return is_face_card
        else:
            is_face_card = False
            return is_face_card
    else:
        pass


# "take turn as normal: put down one card, check for a slap, and then go to the computer


#################################################
def slap(
    player_deck, computer_deck, slappable_deck
):  # might need to split this up again into multiple functions
    ##################### This function needs to run so it can check if there is a slappable card after each card is put down, but will that make the game run slower? what is the optimal way to implement something like this
    # slap list needs to add the most recently played card, and check if there is a duplicate card value in the slappable_deck list
    # if not then do nothing, if there is, there has to be some sort of computer slap function, or maybe that could just be a aprt of this function, that lets the computer know it should slap the deck
    # There should either be a seperate deck for all cards in play, or the function that checks for a slappable hand needs to only look at the three most recent additions to the slappable deck
    slap_pattern_trio = []
    last_three_cards = slappable_deck[-3:]
    for card in last_three_cards:
        slap_pattern_trio.append(card.value)
    if len(slap_pattern_trio) != len(set(slap_pattern_trio)):
        print("slap detected")
        start_time = time.time()  # .after
        computer_reaction_time = random.uniform(2, 4)
        valid_slap = True
        computer_slapped = (
            False  # computer doesn't need to slap until after GUI is set up
        )
        while valid_slap == True and computer_slapped == False:
            if time.time() - start_time >= computer_reaction_time:
                computer_slapped = True
                print("Computer slapped!")
                for card in slappable_deck:
                    computer_deck.insert(0, card)
                slappable_deck.clear()
                return player_deck, computer_deck, slappable_deck
            while not computer_slapped:
                wip_slap = input("Type slap to slap: ")
                if wip_slap == "slap":
                    for card in slappable_deck:
                        player_deck.insert(0, card)
                    slappable_deck.clear()
                    print(
                        f"Yeehaw, you slapped! You have {len(player_deck)} cards now."
                    )
                    return player_deck, slappable_deck, valid_slap
                if wip_slap != "slap":
                    print("what")
                    break
            else:
                print("Computer slapped!")
                for card in slappable_deck:
                    computer_deck.insert(0, card)
                slappable_deck.clear()
                return computer_deck, slappable_deck, valid_slap
    else:
        print("false slap")


# false slap function
"if the player slaps when there is no valid slap, they lose one card, and that card goes to the bottom of the deck, and does not effect the active deck"

# face card function
"if a face card is detected at the top of the deck, the next player must put down the corresponding number of cards in a row, 1 for a jack 2 for a queen, 3 for a king, 4 for an ace"

# gui for the game
"needs to have at least 3 cards showing for the deck that is in play"
"probably would be nice to show more in case there is a face card where there would be up to 5 cards sort of active"
"maybe a number counter or other cards as a visual?"
"need a slap button"

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


# Face card checking code, maybe will be its own function


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
            )


# GUI
####################### figure out how to assign each card image png to each generated card in the code
