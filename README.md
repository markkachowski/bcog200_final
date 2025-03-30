For my project I will be coding the card game slaps. In slaps the entire deck is delt out face-down to about 2-8 players, and the objective is to get cards. Each player takes turns putting one card downn facing up in the center of the table. You are not allowed to look at your cards until they are placed into the center. The main way to get cards is by slapping the deck when there is a certain pattern of card values: doubles or sandwiches. For example two 4s in a row is a double and a queen, a 3, and then a queen is a sandwich. Sandwiches can only be 3 cards long. Once a valid pattern is in play, anyboldy can slap the deck at anytime, and whoever slaps it first, wins all the cards that were put down for that hand. The other way to get cards is explained below in the functions. In addition to the logic and code for the game, I will also be making a UI for it.


Things to include
Slap function: a function that allows the player or the computer to slap when a slap is valid 
User interface: a UI that displays the deck as it moves along, and gives the option to slap and place cards (maybe a slap sound effect too)
Card values: values for all the cards
Face card function: a function for the 4 face cards, which have special rules distinct from the numbered cards. If a face card is played, the next player must put down a certain number of cards in a row. A Jack is 1 card, Queen is 2, King is 3, Ace is 4. If the corresponding number of cards is placed, the player who placed the face card wins that deck. If a face card is placed after another face card i.e. player 1 places an ace, but while putting down the required 4 cards, player 2 places down a queen, it then jumps to player 3, who must now put down 2 cards for player 2's queen. If neither of player 3's cards is a face card, or no slappable pattern occurs, player 2 wins that hand
"False slap" function: a punishment if the player tries to slap the deck when there is no slappable pattern
