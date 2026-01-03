from tkinter import *
import otherFunctions
from playsound import playsound
import os
import random
import time
import fileManager

MAX_CURRENT = 10    #If there are more, new words can't be added manually
MAX_SCORE = 3

#This is where new added words are stored
CURRENT_WORDS_DIR = os.path.join('words','current')
CURRENT_WORDS_PATH = os.path.join(CURRENT_WORDS_DIR,'current_words.json')
WORD_LIST_PATH = os.path.join('words','word_list.json')

#This is where old words are stored
#File naming: DAY-MONTH-YEAR-NUM,
#for example: 02-21-2024-001.json
SHELF_DIR = os.path.join('words','shelf')

IMAGE_FOLDER = "images"
AUDIO_DIR = "audio"

AUDIO_FORMAT = ".mp3"

GAME_DURATION = 300     #10 minutes
CYRILLIC_LETTERS = "йцукенгшщзхъэждлорпавыфячсмитьбюё"
class Ui:
    """
    Creates tkinker interface with buttons and other elements.
    Handle all the features and operations of the main window.
    """
    def __init__(self):
        self.mw = Tk()
        self.mw.title = "lets pelataan"

        self.connection = False

        #Game runtime variables:
        self.word_checked = False
        self.current_fin_word = ""
        self.current_rus_word = ""
        self.current_dict = {}
        self.correct_dict = {}
        self.incorrect_dict = {}
        self.remove_list = []       #A list for words that have reached the max score
        self.time = time.time()
        self.in_test_phase = True

        #Frames
        self.menu_frame = Frame(self.mw)
        self.add_frame = Frame(self.mw)
        self.game_frame = Frame(self.mw)

        self.menu_frame.grid(row= 0,column=0)
        
        # Set window size and center it
        self.mw.geometry("600x400")
        self.mw.update()
        self.mw.resizable(False, False)

        #Menu objects
        self.play_btn = Button(self.menu_frame, text="Pelaa", command=self.start_game)
        self.add_btn = Button(self.menu_frame, text="Lisää sana", command=self.show_add_view)
        self.quit_btn = Button(self.menu_frame, text="Sulje", command=self.mw.destroy)

        self.play_btn.grid(row=0, column=0)
        self.add_btn.grid(row=1, column=0)
        self.quit_btn.grid(row=2, column=0)

        #Word adding objects
        self.return_btn = Button(self.add_frame, text="<-", command=self.show_menu_view)
        self.fin_label = Label(self.add_frame, text="Suomeksi")
        self.rus_label = Label(self.add_frame, text="Venäjäksi")
        self.fin_entry = Entry(self.add_frame)
        self.rus_entry = Entry(self.add_frame)
        self.note_label = Label(self.add_frame, text="") #Tells if addition was succesfull
        self.connection_label = Label(self.add_frame, text="") #Tells if there's internet connection
        self.add_word_btn = Button(self.add_frame, text="Lisää", command=self.add_word)
        self.remove_word_btn = Button(self.add_frame, text="Poista")

        self.added_words_frame = Frame(self.add_frame)
        self.save_words_btn = Button(self.add_frame, text="Tallenna sanat")

        self.return_btn.grid(row=0, column=0)
        self.fin_label.grid(row=1, column=0)
        self.rus_label.grid(row=1, column=1)
        self.fin_entry.grid(row=2, column=0)
        self.rus_entry.grid(row=2, column=1)
        self.note_label.grid(row=3, column=0)
        self.connection_label.grid(row=4, column=0)
        self.add_word_btn.grid(row=5, column=0)
        self.remove_word_btn.grid(row=5, column=1)
        self.added_words_frame.grid(row=6, column=0)
        self.save_words_btn.grid(row=7, column=0)

        #Game Objects
        self.stop_game_button = Button(self.game_frame, text="<-", command=self.end_game)
        self.img_holder = Label(self.game_frame)
        self.asked_word = Label(self.game_frame, text="")
        self.answer_entry = Entry(self.game_frame)
        self.sound_button = Button(self.game_frame, text="Kuuntele", command=self.pronounce_russian)
        self.check_button = Button(self.game_frame, text="Seuraava", command=self.check_or_fetch_new)
        self.time_label = Label(self.game_frame, text="00:00")

        self.stop_game_button.grid(row=0, column=0)
        self.img_holder.grid(row=1, column=0)
        self.img_holder.grid(row=2, column=0)
        self.asked_word.grid(row=3, column=0)
        self.answer_entry.grid(row=4, column=0)
        #self.sound_button.grid(row=5, column=0)
        self.check_button.grid(row=6, column=0)
        self.time_label.grid(row=7,column=0)

        #Make sure necessary folders exist
        fileManager.create_directories([SHELF_DIR, CURRENT_WORDS_DIR, IMAGE_FOLDER, AUDIO_DIR])     

    def show_add_view(self):
        self.menu_frame.grid_forget()
        self.add_frame.grid(row=0,column=0)

    def show_menu_view(self):
        self.add_frame.grid_forget()
        self.game_frame.grid_forget()
        self.menu_frame.grid(row=0,column=0)

        self.word_checked = False
        self.current_fin_word = ""
        self.current_rus_word = ""
        self.current_dict = {}
        self.correct_dict = {}
        self.incorrect_dict = {}

    '''
    Remove image, colors, listening button, etc
    '''
    def reset_game_view(self):
        self.game_frame.config(bg="white")
        self.check_button.config(text="Tarkista")
        self.sound_button.grid_forget()
    def start_game(self):
        self.menu_frame.grid_forget()
        self.game_frame.grid(row=0, column=0)

        # Gather word data: (some added new words and some old words (and data related to them))
        self.current_dict = otherFunctions.gather_data(CURRENT_WORDS_PATH,SHELF_DIR, MAX_CURRENT)

        #Start running the game if any words were found
        if (len(self.current_dict) != 0):
            self.time = time.time()
            self.time_label.config(text=(time.time()- self.time))
            self.ask_new_word()
        else:
            print("New words must be added manually!")
            self.show_menu_view()

    def end_game(self):
        self.word_checked = False
        self.current_fin_word = ""
        self.current_rus_word = ""
        self.current_dict = {}
        self.correct_dict = {}
        self.incorrect_dict = {}
        self.remove_list = []
        self.in_test_phase = True
        self.reset_game_view()
        self.show_menu_view()

    def ask_new_word(self):
        self.current_fin_word = random.choice(list(self.current_dict.keys()))
        self.current_rus_word = self.current_dict[self.current_fin_word][0]
        self.answer_entry.delete(0, 'end')
        self.asked_word.config(text=self.current_fin_word)
        self.word_checked = False

        # Show the image if found
        otherFunctions.show_image(self.current_fin_word, IMAGE_FOLDER, self.img_holder)

        # Set the appearance of the UI
        self.reset_game_view()


    def times_up(self):
        if(time.time()- self.time > GAME_DURATION):
            print("Time's up!")
            return True
        else:
            print("Time remaining")
            return False

    def reduce_score(self):
        score = self.current_dict[self.current_fin_word][1]
        if (score > 0):
            score -= 1
        self.incorrect_dict[self.current_fin_word] = [self.current_rus_word, score]

    '''
    If the score of the word is lower than MAX_SCORE-1 the score will be increased and
    stored in the correct_dict.
    Otherwise the word will be added to the remove_list.
    '''
    def increase_score(self):
        score = self.current_dict[self.current_fin_word][1]
        if (score < MAX_SCORE-1):
            score += 1
            self.correct_dict[self.current_fin_word] = [self.current_rus_word, score]
        else:
            self.remove_list.append(self.current_fin_word)

    def show_time(self):
        time_elapsed = (time.time() - self.time)
        minutes_elapsed = int(time_elapsed/60)
        seconds_elapsed = round(time_elapsed%60)
        time_digits = f"{minutes_elapsed:02}:{seconds_elapsed:02}"
        print("Timer: ", time_digits)
        self.time_label.config(text=time_digits)

    def check_word(self):
        self.word_checked = True
        entry = self.answer_entry.get().strip()

        # Wrong answer
        if(entry != self.current_rus_word):
            print("wrong answer")
            # Set background color and show right answer
            self.game_frame.config(bg="orange")
            self.asked_word.config(text=self.current_rus_word)

            # Set score, and mark the word as incorrect, if in the exam phase
            if (self.in_test_phase):
                self.reduce_score()

        #Right answer
        else:
            if(self.in_test_phase):
                self.increase_score()

            self.game_frame.config(bg="green")

    def save_progress(self):
        # Remove all the needed words from the list file
        word_list = fileManager.read_json(WORD_LIST_PATH)
        for word in self.remove_list:
            i = word_list.index(word)
            word_list.pop(i)

            #remove audio files too
            audio_file = os.path.join(AUDIO_DIR,word+AUDIO_FORMAT)
            print(f"removing an audio file: {audio_file}")
            fileManager.delete_file(audio_file)

        fileManager.write_json(word_list, WORD_LIST_PATH)
        self.remove_list = []

        # Put words that got answered wrong to current.json
        fileManager.new_file_json(CURRENT_WORDS_PATH)
        fileManager.write_json(self.incorrect_dict, CURRENT_WORDS_PATH)

        # Put right answers to shelf
        #print("right answers after round: ", self.correct_dict)
        if(len(self.correct_dict) > 0):
            fileManager.store_in_shelf(self.correct_dict, SHELF_DIR)

    def enter_rehearse_phase(self):
        # Start revising the words that went wrong (if there are any)
        self.in_test_phase = False
        self.current_dict = self.incorrect_dict

    def check_or_fetch_new(self):
        #Check the word
        if(not self.word_checked):
            self.check_word()

            # add the listen button
            self.sound_button.grid(row=5, column=0)
            self.check_button.config(text="Seuraava")

        # Fetch a new word
        else:
            if(self.in_test_phase):

                #Remove the asked word from currents
                del self.current_dict[self.current_fin_word]

                # Fetch a new word
                if (len(self.current_dict) != 0):
                    print("fetching new word")
                    self.ask_new_word()

                # All the words are asked: save the progres, and enter the rehearing phase
                else:
                    print("entering the rehearse phase")
                    self.save_progress()
                    self.enter_rehearse_phase()
                    if (len(self.current_dict) != 0):
                        self.ask_new_word()

            #Game is in the rehearse phase: ask new words until the time ends
            elif(not self.in_test_phase and not self.times_up()):
                self.show_time()
                if (len(self.current_dict) == 0):
                    self.end_game()
                    return
                self.ask_new_word()

            # Time's up (in the test phase)
            else:
                self.end_game()

    def accept_new_word(self, fin_word, rus_word):
        # Check that entries are not empty
        if fin_word == "" or rus_word == "":
            self.note_label.config(text="Täytä kaikki laatikot")
            return False

        # Make sure normal alphabet and cyrillic are in the correct boxe
        for c in rus_word:
            if (c not in CYRILLIC_LETTERS) and c != ' ':
                return False

        return True

    """
    * Add a word to the game, if it doesn't already exist.
    * Create audio file for the russian word
    """
    def add_word(self):
        # Get the user written words
        finnish_word = self.fin_entry.get().strip()
        russian_word = self.rus_entry.get().strip()
        # lowercase everything
        finnish_word.lower()
        russian_word.lower()

        #Check input
        if(self.accept_new_word(finnish_word, russian_word)!=True):
            return

        word_dict = fileManager.read_json(CURRENT_WORDS_PATH)
        word_list = fileManager.read_json(WORD_LIST_PATH, True)

        # Make sure directory is not full
        if len(word_dict) >= MAX_CURRENT:
            self.note_label.config(text="Tiedosto täynnä max: " + str(MAX_CURRENT) + "sanaa.")
            return False

        # Check if the word already exists in the game
        if finnish_word in word_list:
            self.note_label.config(text="Sana on jo tiedostossa current.json")
            return False

        # Add the word to the dictionary and the word list
        word_dict[finnish_word] = [russian_word,0]
        word_list.append(finnish_word)

        # Write in the current.json and word_list.json new data
        fileManager.write_json(word_dict, CURRENT_WORDS_PATH)
        fileManager.write_json(word_list, WORD_LIST_PATH)

        #add audio file for the russian word
        fileManager.create_russian_audio(russian_word, finnish_word, AUDIO_DIR)

        # Inform the user about successful action
        self.note_label.config(text="Sana lisätty")
        self.rus_entry.delete(0, 'end')
        self.fin_entry.delete(0, 'end')
        print(f'word "{finnish_word}" added')

    """
    Search an audio file with a name {fiWord} and play it
    """
    def pronounce_russian(self):
        path = os.path.join("audio", f"{self.current_fin_word}.mp3")
        playsound(path)

    def start(self):
        self.mw.mainloop()


def main():
    ui = Ui()
    ui.start()


if __name__ == "__main__":
    main()