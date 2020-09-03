#Fixes bug to delete previous guesses from past game every reset.
#Fixes bug so colours of hint buttons revert back to blue every reset.
#Fixes bug so score_label shows 100 after every reset.
#Adds "Are you sure?" before reset
#Subtract score by 1 for every wrong attempts for hard mode.

#Primality bug remains

from tkinter import *
import random, math
from tkinter import messagebox

root = Tk()
root.title("Number Guessing Game")

#Initializes attempt count to 1 and score to 100
attempt_count = 0
score = 100
#String to store previous guesses
prev_attempts = str()
#Boolean to reset GUI if user chooses replay
replay_status = False

#Function to update score:
def updatescore(x):
    global score
    score = score - x
    score_label.config(text = "Current score: " + str (score))

#Functions for hints
def digitcount():
    hint_button7.config (text = "The number has "+ str (len(str(compnum))) + " digits.", fg = "black", state = DISABLED)
    updatescore (5)
def digittenths():
    hint_button6.config (text = "The digit in the\ntenths place is " + str(compnum)[len(str(compnum))-1] + ".", fg = "black", state = DISABLED)
    updatescore (15)
def fibonacci():
    fibonacci_list = [0,1]
    i = 0
    while max(fibonacci_list) < difficulty:
        x = fibonacci_list[i] + fibonacci_list[i+1]
        fibonacci_list.append(x)
        i = i + 1
    if compnum in fibonacci_list:
        hint_button9.config (text = "The number is\nin the Fibonacci sequence.", fg = "black", state = DISABLED)
    else:
        hint_button9.config (text = "The number is not\nin the Fibonacci sequence.", fg = "black", state = DISABLED)
    updatescore (5)
def isodd():
    if compnum % 2 == 0:
        hint_button2.config(text = "The number is even.", fg = "black", state = DISABLED)
    else:
        hint_button2.config(text = "The number is odd.", fg = "black", state = DISABLED)
    updatescore (15)
def median_compare ():
    if compnum <= difficulty / 2:
        hint_button1.config (text = "The number is less than\nor equal to " + str (int(difficulty/2)) + ".", fg = "black", state = DISABLED)
    else:
        hint_button1.config (text = "The number is more than " + str (int(difficulty/2)) + ".", fg = "black", state = DISABLED)
    updatescore (20)
#BUGGY
def primality():
    if compnum % 2 == 0:
        hint_button8.config (text = "Number is not prime", fg = "black", state = DISABLED)
    else:
        for i in range (3, int(compnum/2) + 1, 2):
            if compnum % i == 0:
                hint_button8.config (text = "Number is not prime", fg = "black", state = DISABLED)
                break
            elif i == int(compnum/2) or int(compnum/2) + 1:
                hint_button8.config (text = "Number is prime", fg = "black", state = DISABLED)
    updatescore (5)
def isquintet ():
    if compnum % 5 == 0:
        hint_button4.config (text = "The number is\na multiple of 5.", fg = "black", state = DISABLED)
    else:
        hint_button4.config (text = "The number is\nnot a multiple of 5.", fg = "black", state = DISABLED)
    updatescore (10)
def issquare():
    if math.sqrt (compnum).is_integer() == True:
        hint_button5.config (text = "The number is a square.", fg = "black", state = DISABLED)
    else:
        hint_button5.config (text = "The number is not a square.", fg = "black", state = DISABLED)
    updatescore (5)
def istriplet ():
    if compnum % 3 == 0:
        hint_button3.config (text = "The number is\na multiple of 3.", fg = "black", state = DISABLED)
    else:
        hint_button3.config (text = "The number is\nnot a multiple of 3.", fg = "black", state = DISABLED)
    updatescore (10)

#Function to generate computer's number by using user's chosen difficulty
def assign_difficulty(x):
    global compnum
    global difficulty

    #Disables all difficulty
    for i in difficulty_tuple:
        i.config (state = DISABLED)

    #Colors the chosen difficulty button
    if x == 0:
        difficulty_button1.config (disabledforeground = "green")
        difficulty = 10
    if x == 1:
        difficulty_button2.config (disabledforeground = "blue")
        difficulty = 100
    if x == 2:
        difficulty_button3.config (disabledforeground = "red")
        difficulty = 1000

    compnum = random.randint(1,difficulty)
    answer_entry.config (state = NORMAL)
    answer_button.config (state = NORMAL)
    for i in hint_buttontuple:
        i.config (state = NORMAL)

def bubblesort(x):
    x = x.split()
    print
    #To count how many swaps are done in each round
    swapcount = 0

    #Loops until no swaps are made
    while True:
        #Each round, iterate from 0 to i - 1
        for i in range(len (x) - 1):
            #Tuple to compare
            comparer = (x[i],x[i+1])
            #If previous element is greater, swap
            if comparer [0] > comparer [1]:
                x [i] = comparer [1]
                x [i+1] = comparer [0]
                #To check how many swaps are done this round
                swapcount = swapcount + 1
        if swapcount == 0:
            break
        #After each round, if list still unsorted, initializes swapcount to 0 for use in further round
        swapcount = 0
    return " ".join(x)

#Disables multiple buttons
def disable_button():
    answer_entry.config(state = DISABLED)
    answer_button.config (state = DISABLED)
    for i in hint_buttontuple:
        i.config (state = DISABLED)

#For reset
def replay():
    response = messagebox.askquestion ("Number Guessing Game", "Are you sure you want to replay?")
    if response == 0:
        return
    else:
        disable_button()
        global attempt_count, score, prev_attempts, compnum, difficulty,replay_status,result
        #Initializes these variables to 0
        attempt_count = compnum = difficulty = 0
        #Deletes previous guesses from past game
        attempt_label.config(text = "Previous guesses: ")
        prev_attempts = str()
        #Initializes score to 0
        score = 100
        score_label.config (text = "Current score: 100")
        #Recovers hint buttons text and reverts colour to blue
        for i in range(len(hint_buttontuple)):
            hint_buttontuple[i].config (text = original_hintbuttons[i], fg = "blue")
            #Deletes user outcome from past game
            result.config(text = "Come on! Use that smart brain!")
            #Makes disabledforeground of difficulty buttons back to grey
            for i in difficulty_tuple:
                i.config(state = NORMAL, disabledforeground = "grey")

#Asks user to input an integer and check its validity. If not, repromts the user
def userplay(x):
    #Enables manipulation of the following global variables
    global attempt_count, score, prev_attempts
    x = x.strip()
    #Checks whether x is an integer
    try:
        x = int (x)
        #Checks whether x is in range
        if 0 < x <= difficulty:
            if str(x) in prev_attempts.split():
                answer_entry.delete(0,END)
                answer_entry.insert(0, "You have inputted this integer. Try another.")
            else:
                usernum = x
                answer_entry.delete (0, END)
        else:
            answer_entry.delete(0,END)
            answer_entry.insert(0, "Please input an integer between 0 and " + str(difficulty))
    #Prints an error message in case of bad input
    except:
        answer_entry.delete(0,END)
        answer_entry.insert(0, "Please input an integer.")

    #Determines whether user succeeds and prints score
    if usernum == compnum:
        result.config(text = "Congratulations! You guessed correctly. Your score is " + str (score))
        #Ensures user cannot enter or press hints anymore after they win
        disable_button()
    else:
        if difficulty == 10:
            updatescore (10)
        elif difficulty == 100:
            updatescore (5)
        else:
            updatescore (1)
        #Updates status variables and shows it onto GUI
        attempt_count = attempt_count + 1
        prev_attempts = prev_attempts + str(usernum) + " "
        attempt_label.config (text = "Previous guesses: " + bubblesort(prev_attempts))
        #What happens if user loses
        if score <= 0:
            result.config(text = "Sorry. You lose. The number was " + str (compnum))
            disable_button()
        if score <= 10:
            for i in hint_buttontuple:
                i.config (state = DISABLED)


#Intro Label
intro_label = Label (root, width = 60, text = "Hello! Welcome to a Number Guessing Game.\nWe will generate a random number in according to your desired difficulty.\nThen, you will try to guess with the help of our hints.")
intro_label.grid(row = 0, column = 0, columnspan = 6,)


#Difficulty widgets
difficulty_label = Label(root, width = 60, text= "Please type the number that corresponds to your desired difficulty!")
difficulty_button1 = Button (root, width = 20, height = 5, text = "Easy\n (1-10)", command = lambda: assign_difficulty(0))
difficulty_button2 = Button (root, width = 20, height = 5, text = "Normal\n (1-100)", command = lambda: assign_difficulty(1))
difficulty_button3 = Button (root, width = 20, height = 5, text = "Hard\n (1-1000)", command = lambda: assign_difficulty(2))

difficulty_label.grid(row = 1, column = 0, columnspan = 6)
difficulty_button1.grid(row = 2, column = 0, padx = 5, columnspan = 2)
difficulty_button2.grid(row = 2, column = 2, padx = 5, columnspan = 2)
difficulty_button3.grid(row = 2, column = 4, padx = 5, columnspan = 2)
difficulty_tuple = (difficulty_button1, difficulty_button2, difficulty_button3)


#Answer widgets
answer_entry = Entry(root, width = 41, state = DISABLED)
answer_entry.insert(0,"Input your answer here!")
answer_button = Button(root, width = 20, text = "->", command = lambda : userplay(answer_entry.get()), state = DISABLED)

answer_entry.grid(row = 3, column = 0, columnspan = 4)
answer_button.grid (row = 3, column = 4, columnspan = 2)


#Hints widgets
hint_label = Label(root, text= "Available Hints")
hint_button1 = Button (root, text = "Is the number greater or\nless than the median?\n(-15)", command = median_compare)
hint_button2 = Button (root, text = "Is the number odd or even?\n(-15)", command = isodd)
hint_button3 = Button (root, text = "Is the number a\nmultiple of 3?\n(-10)", command = istriplet)
hint_button4 = Button (root, text = "Is the number a\nmultiple of 5?\n(-10)", command = isquintet)
hint_button5 = Button (root, text = "Is the number a square?\n(-5)", command = issquare)
hint_button6 = Button (root, text = "What is the digit\nin the tenths place?\n(-10)", command = digittenths)
hint_button7 = Button (root, text = "How many digits\ndoes the number contain?\n(-5)", command = digitcount)
hint_button8 = Button (root, text = "Is the number a prime?\n(-5)", command = primality)
hint_button9 = Button (root, text = "Is the number in the\nFibonacci sequence?\n(-5)", command = fibonacci)


#A list of hint buttons that can be used to easily configure their properties
hint_buttontuple = (hint_button1, hint_button2, hint_button3, hint_button4, hint_button5, hint_button6, hint_button7, hint_button8, hint_button9)
#A tuple of original hint buttons that is used to preserve the text. Main use is for reset
original_hintbuttons = (
    "Is the number greater or\nless than the median?\n(-15)",
    "Is the number odd or even?\n(-15)",
    "Is the number a\nmultiple of 3?\n(-10)",
    "Is the number a\nmultiple of 5?\n(-10)",
    "Is the number a square?\n(-5)",
    "What is the digit\nin the tenths place?\n(-10)",
    "How many digits\ndoes the number contain?\n(-5)",
    "Is the number a prime?\n(-5)",
    "Is the number in the\nFibonacci sequence?\n(-5)"
    )

for i in hint_buttontuple:
    i.config (width = 20, height = 5, state = DISABLED, fg = "blue")

hint_label.grid(row = 4, column = 0, columnspan = 6)
hint_button1.grid(row = 5, column = 0, columnspan = 2)
hint_button2.grid(row = 5, column = 2, columnspan = 2)
hint_button3.grid(row = 5, column = 4, columnspan = 2)
hint_button4.grid(row = 6, column = 0, columnspan = 2)
hint_button5.grid(row = 6, column = 2, columnspan = 2)
hint_button6.grid(row = 6, column = 4, columnspan = 2)
hint_button7.grid(row = 7, column = 0, columnspan = 2)
hint_button8.grid(row = 7, column = 2, columnspan = 2)
hint_button9.grid(row = 7, column = 4, columnspan = 2)


#Labels for displaying current scores and logs previous attempts made by the user
attempt_label = Label (root, width = 40, text = "Previous guesses: ")
score_label = Label (root, width = 20, text = "Current score: 100")

attempt_label.grid (row = 8, column = 0, columnspan = 4)
score_label.grid(row = 8, column = 4, columnspan = 2)


#Label to indicate to user whether they won or lost. However, initialized to an encouraging message.
result = Label (root, text = "Come on! Use that smart brain!")
result.grid(row = 9, column = 0, columnspan = 6)
disable_button()


#Creates replay button
replay_button = Button (root, text = "Replay?", width = 60, height = 5, command = replay)
replay_button.grid (column = 0, row = 10, columnspan = 6)


root.mainloop()
