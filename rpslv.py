import random
import os

# Seeds Random number generator with System Time.
random.seed()

# Global Variable Declarations
level = 0
player = 0
computer = 0
game = 0
win = 0
playerScore = 0
computerScore = 0
computerResult = ""
playerResult = ""
gameResult = ""

# Clears the terminal and prints the Welcome Message.
def clear():
    os.system('cls' if os.name=='nt' else 'clear')
    print("Welcome to RPSLV!")

# Prints the Score to the screen.
def getScore():
    global playerScore
    global computerScore
    if playerScore == 0 and computerScore == 0:
        return("No Score")
    else:
        return("Player: " + str(playerScore) + " | Computer: " + str(computerScore))

# Prompts the Player to select Easy or Hard mode.
def setDifficulty():
    global level

    isValid = False
    while not isValid:

        levelStr = ""
        levelStr = input("Would you like Easy or Hard: ")
        levelStr = levelStr.lower()

        # Assigns number based on input for further processing.
        if levelStr == "easy":
            level = 1
        elif levelStr == "hard":
            level = 2
        else:
            clear()
            level = 0
            print("That is not a Valid Selection!")

        # If the number assigned is easy or hard, isValid is True.
        if level == 1 or level == 2:
            isValid = True

# Main Game Selection
# Prompts the User for input based on the difficulty selected.
# The Default option is easy.
def playGame(level=1):
    isValid = False
    while not isValid:
        playerStr = ""

        if level == 1:
            playerStr = input("Please Enter 'rock', 'paper', 'sissors', 'exit': ")
        elif level == 2:
            playerStr = input("Please Enter 'rock', 'paper', 'sissors', 'lizard', 'spock', 'exit': ")
        else:
            print("Error, Difficulty Not Set!")
            exit()

        playerStr = playerStr.lower()
        global player
        global computer

        # print(playerStr)
        # Assigns number based on input for further processing.
        if playerStr == "rock":
            player = 1
        elif playerStr == "paper":
            player = 2
        elif playerStr == "sissors":
            player = 3
        elif playerStr == "lizard":
            player = 4
        elif playerStr == "spock":
            player = 5
        elif playerStr == "exit" or playerStr == "quit":
            clear()
            print("Final Score ~ " + getScore())
            print("Goodbye")
            exit()
        else:
            clear()
            player = 0
            print("That is not a Valid Selection!")

        # If the number assigned is between 1 and 5, isValid is True.
        if player >= 1 and player <= 5:
            isValid = True

    # Easy
    if level == 1:
        computer = random.randint(1,3)
    # Hard
    elif level == 2:
        computer = random.randint(1,5)

    #Debug Number Generator
    #print(computer)
    #print(player)

# Main Game Algorithm
# Uses the number assigned from the input of the user
# and the Random number generated for the computer
# and determines the result of the game
def getGameResult(c, p):
    global computerResult
    global game
    global win

    if c == 1:
        computerResult = "The Computer chose Rock"
        if p == 1:
            game = 0
            win = 0
        elif p == 2:
            game = 2
            win = 1
        elif p == 3:
            game = 10
            win = 2
        elif p == 4:
            game = 3
            win = 2
        elif p == 5:
            game = 9
            win = 1
    elif c == 2:
        computerResult = "The Computer chose Paper"
        if p == 1:
            game = 2
            win = 2
        elif p == 2:
            game = 0
            win = 0
        elif p == 3:
            game = 1
            win = 1
        elif p == 4:
            game = 7
            win = 1
        elif p == 5:
            game = 8
            win = 2
    elif c == 3:
        computerResult = "The Computer chose Sissors"
        if p == 1:
            game = 10
            win = 1
        elif p == 2:
            game = 1
            win = 2
        elif p == 3:
            game = 0
            win = 0
        elif p == 4:
            game = 6
            win = 2
        elif p == 5:
            game = 5
            win = 1
    elif c == 4:
        computerResult = "The Computer chose Lizard"
        if p == 1:
            game = 3
            win = 1
        elif p == 2:
            game = 7
            win = 2
        elif p == 3:
            game = 6
            win = 1
        elif p == 4:
            game = 0
            win = 0
        elif p == 5:
            game = 4
            win = 2
    elif c == 5:
        computerResult = "The Computer chose Spock"
        if p == 1:
            game = 9
            win = 2
        elif p == 2:
            game = 8
            win = 1
        elif p == 3:
            game = 5
            win = 2
        elif p == 4:
            game = 4
            win = 1
        elif p == 5:
            game = 0
            win = 0

# Assigns a String based on the number assigned from the result of the Game
def getWinResult(g, p):
    global playerResult
    global gameResult
    global playerScore
    global computerScore

    if g == 0:
        gameResult = "It's a Tie!"
    elif g == 1:
        gameResult = "Scissors cut Paper"
    elif g == 2:
        gameResult = "Paper covers Rock"
    elif g == 3:
        gameResult = "Rock crushes Lizard"
    elif g == 4:
        gameResult = "Lizard poisons Spock"
    elif g == 5:
        gameResult = "Spock smashes Scissors"
    elif g == 6:
        gameResult = "Scissors decapitate Lizard"
    elif g == 7:
        gameResult = "Lizard eats Paper"
    elif g == 8:
        gameResult = "Paper disproves Spock"
    elif g == 9:
        gameResult = "Spock vaporizes Rock"
    elif g == 10:
        gameResult = "Rock crushes Scissors"

    # If a Tie, no points are earned.
    if p == 0:
        playerResult = "Nobody Wins"
    # Player Wins and earns 1 point.
    elif p == 1:
        playerResult = "You Win!"
        playerScore += 1
    # Computer Wins and earns 1 point.
    elif p == 2:
        playerResult = "You Lose!"
        computerScore += 1

clear()
setDifficulty()
clear()

# Main Game Loop
while True:
    playGame(level)
    clear()
    getGameResult(computer, player)
    getWinResult(game, win)
    print(computerResult)
    print(gameResult)
    print(playerResult)
    print(getScore())
