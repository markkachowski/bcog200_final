For my project I coded the card game slaps. In slaps the entire deck is delt out face-down to about 2-8 players, and the objective is to get cards. Each player takes turns putting one card down facing up in the center of the table. You are not allowed to look at your cards until they are placed into the center. The main way to get cards is by slapping the deck when there is a certain pattern of card values: doubles or sandwiches. For example two 4s in a row is a double, and a queen, a 3, and then a queen is a sandwich. Sandwiches can only be 3 cards long. In this version you can also slap when a jack is placed. Once a valid pattern is in play, anybody can slap the deck at anytime, and whoever slaps it first, wins all the cards that were put down for that hand. In addition to the logic and code for the game, I also made a GUI for it.



Here is a rundown of the code, the script file contains notes on each method in each class

Slap method: a function that allows the player or the computer to slap when a slap is valid.

Graphical User interface: a GUI that displays the relevant deck as it moves along, and gives the option to slap and place cards.

Card values: values for all the cards.

Originally I was going to add a face card function, but after playing slaps in real life, I decided not to finish it. The main reason for this is that the game would never end. With only 2 players, the face cards add in a huge luck factor, and reduce the skill factor. When playing with a group of people it's fine, but when it gets down to the last two it just never ends. Instead of this, I made jacks slappable, which makes slaps more frequent, and also allows either the player or computer to actually win.

"False slap" method: a punishment if the player tries to slap the deck when there is no slappable pattern, this ended up being part of the slap method.

Card images: I got the images for the playing cards here https://code.google.com/archive/p/vector-playing-cards/downloads

Also included are:
3 difficulties with quicker reaction times and a progressively smaller slap button, and the mean time it took for you to slap, displayed for you once you win or lose


To run the game you need script_file.py or test_file.py, and the images folder that contains all the card images and they both need to be in the same folder.
