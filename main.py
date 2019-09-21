import tkinter as tk
import random


# global constants
TOTAL_TIME = 60
SCORE = 0
RUNNING = False
LETTERS = 0



# game functions
def countdown():
    '''Decrements time by 1 after each second and reconfigures application visuals'''

    global TOTAL_TIME
    global SCORE
    global LETTERS

    if TOTAL_TIME > 0 and RUNNING:
        TOTAL_TIME -= 1
        timeLabel.config(text="Time Remaining: " + str(TOTAL_TIME))
        timeLabel.after(1000, countdown)
    elif TOTAL_TIME == 0:
        retry.config(text="Press Enter to reset")
        letterLabel.config(text="WPM: " + str((LETTERS/5)))
        root.bind("<Return>", reset_game)


def scrape_words():
    '''returns a list of 1000 most commonly used words'''

    with open("words.txt") as w:
        ls = w.read().rstrip("\n").split()
    return ls


def modify_words(event=None):
    '''Deletes the first word and appends a new one'''
    global RUNNING
    if TOTAL_TIME > 0 and RUNNING:
        add_score()
        WORD_LIST.pop(0)
        WORD_LIST.append(scrape_words()[random.randint(0,995)])
        wordLabel.config(text=' '.join(WORD_LIST))
        root.bind("<space>", modify_words)


def get_word():
    '''helper method to create a list of words'''
    word_list = scrape_words()
    return [word_list[random.randint(0,995)] for x in range(20)]


def get_first_words():
    '''generates random word string'''
    w = get_word()
    out = ' '.join(w)
    wordLabel.config(font="12", text=out)
    return w


def clear_entry():
    '''clears the entry box'''
    entry.delete(0, tk.END)


def add_score():
    '''add one to the overall score if matching'''
    global SCORE
    global LETTERS

    if entry.get()[0:-1] == WORD_LIST[0]:
        SCORE += 1
        LETTERS += len(WORD_LIST[0])
        score.config(text="Score: " + str(SCORE))
    clear_entry()


def begin_game(event=None):
    '''begins the countdown, score calculations, and text modification'''
    global RUNNING
    RUNNING = True

    if TOTAL_TIME == 60:
        root.bind("<space>", modify_words)
        countdown()
        retry.config(text="")


def reset_game(entry=None):
    '''resets game to default settings'''

    global SCORE
    global TOTAL_TIME
    global WORD_LIST
    global RUNNING

    SCORE = 0
    TOTAL_TIME = 60
    WORD_LIST = get_first_words()
    LETTERS = 0

    score.config(text=str(SCORE))
    timeLabel.config(text="Time Remaining: " + str(TOTAL_TIME))
    letterLabel.config(text="")

    clear_entry()
    RUNNING = False
    root.bind("<KeyPress>", begin_game)


# main driver
# setup
root = tk.Tk()
root.title("Typing Test")
root.geometry("440x180")

# instructions text
instructions = tk.Label(root, text="To begin, start typing", font="30")
instructions.pack()

# score
score = tk.Label(root, text="Score: " + str(SCORE), font="12")
score.pack()

# timer
timeLabel = tk.Label(root, text="Time Remaining: " + str(TOTAL_TIME), font="12")
timeLabel.pack()

# word entry
entry = tk.Entry(root, font="12")
entry.pack(fill="both",side="bottom")
entry.focus_set()

# word display
wordLabel = tk.Label(root, background="yellow", anchor="w")
WORD_LIST = get_first_words()
wordLabel.pack(fill="both", side="bottom")

# letters per minute
letterLabel = tk.Label(root)
letterLabel.pack(side="left")

# retry message
retry = tk.Label(root)
retry.pack(side="right")




root.bind("<KeyPress>", begin_game)
root.mainloop()
