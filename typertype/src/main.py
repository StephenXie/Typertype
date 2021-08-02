import curses
import random
import time
import json
import os
import sys
from .word_modification import *
from .read_settings import *
# Credits to Curses python library and https://docs.python.org/3/howto/curses.html for basic command line interface control.
# Credits to JSON python library and https://docs.python.org/3/library/json.html for reading and writing JSON files.


class Typer_base:
    def __init__(self, stdscr):
        self.WIN_Y, self.WIN_X = stdscr.getmaxyx()
        self.Y, self.X = self.WIN_Y // 2, 5
        self.set_colors(stdscr)
        curses.curs_set(False)
        self.settings = get_settings()
        self.WORDS_PER_SET = settings.get("WORDS_PER_SET", 20)
        self.CORRECTIONS = settings.get("CORRECTIONS", "None")
        self.TEST_TIMER = settings.get("TEST_TIMER", 60)
        self.SPACE_STOP = settings.get("SPACE_STOP", True)
        self.WORD_MODIFICATION = settings.get("WORD_MODIFICATION", "Normal")
        self.words = []
        # The text file contains a list of common English words
        with open(filename, "r") as reader:
            for line in reader:
                self.words.append(line.replace("\n", ""))

    def Settings(self, stdscr):
        stdscr.clear()
        arrow_x = self.WIN_X // 2 + 12
        arrow_y = 1
        stdscr.refresh()
        while True:
            self.center_text(stdscr, "Settings", self.WIN_Y//12)
            self.center_text(
                stdscr, f"Words Per Set: {self.WORDS_PER_SET} words", self.WIN_Y//6)
            self.center_text(
                stdscr, f"Corrections: {self.CORRECTIONS}", 2*self.WIN_Y//6)
            self.center_text(
                stdscr, f"Test Timer: {self.TEST_TIMER} seconds", 3*self.WIN_Y//6)
            self.center_text(
                stdscr, f"Space Stop: {self.SPACE_STOP}", 4*self.WIN_Y//6)
            self.center_text(
                stdscr, f"Word Modification: {self.WORD_MODIFICATION}", 5*self.WIN_Y//6)
            if arrow_y == 1:
                cur_key, self.WORDS_PER_SET = self.set_option(stdscr, "Words per set", [
                    5, 10, 15, 20, 25, 30, 35, 40, 45, 50], self.WIN_Y//6, self.WORDS_PER_SET, "words")
            elif arrow_y == 2:
                cur_key, self.CORRECTIONS = self.set_option(
                    stdscr, "Corrections", ["None", "Backspace", "Stop"], 2*self.WIN_Y//6, self.CORRECTIONS)
            elif arrow_y == 3:
                cur_key, self.TEST_TIMER = self.set_option(stdscr, "Test timer", [
                    10, 15, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300], 3*self.WIN_Y//6, self.TEST_TIMER, "seconds")
            elif arrow_y == 4:
                cur_key, self.SPACE_STOP = self.set_option(
                    stdscr, "Space stop", [True, False], 4*self.WIN_Y//6, self.SPACE_STOP)
            elif arrow_y == 5:
                cur_key, self.WORD_MODIFICATION = self.set_option(stdscr, "Word modification", [
                    "None", "Weak", "Normal", "Strong", "Extreme", "???"], 5*self.WIN_Y//6, self.WORD_MODIFICATION)
            else:
                cur_key = stdscr.getch()
            if cur_key == curses.KEY_DOWN or cur_key == ord('s'):
                arrow_y += 1
                arrow_y %= 6
                if arrow_y == 0:
                    arrow_y = 1
            elif cur_key == curses.KEY_UP or cur_key == ord('w'):
                arrow_y -= 1
                arrow_y %= 6
                if arrow_y == 0:
                    arrow_y = 5
            elif cur_key == 27 or cur_key == curses.KEY_COPY or cur_key == curses.KEY_END or cur_key == curses.KEY_BREAK:
                return
            stdscr.clear()
            stdscr.refresh()

    def set_option(self, stdscr, name, options, y, cur, message=""):
        global settings
        i = options.index(cur)
        var_name = name.replace(" ", "_").upper()
        if message != "":
            self.center_text(
                stdscr, f"< {name.title()}: {options[i]} {message} >", y)
        else:
            self.center_text(stdscr, f"< {name.title()}: {options[i]} >", y)
        cur_key = stdscr.getch()
        while True:
            self.clr_cur_line(stdscr, y)
            if cur_key == curses.KEY_LEFT or cur_key == ord("a"):
                i -= 1
                i = i % len(options)
            elif cur_key == curses.KEY_RIGHT or cur_key == ord("d"):
                i += 1
                i = i % len(options)
            else:
                return cur_key, settings[var_name]
            if message:
                self.center_text(
                    stdscr, f"< {name.title()}: {options[i]} {message} >", y)
            else:
                self.center_text(
                    stdscr, f"< {name.title()}: {options[i]} >", y)
            settings[var_name] = options[i]
            cur_key = stdscr.getch()

    def clr_cur_line(self, stdscr, y):
        stdscr.addstr(y, 0, " "*self.WIN_X)
        stdscr.refresh()

    def center_text(self, stdscr, text, y=None, attr=None):
        if y == None:
            y = self.WIN_Y//2
        if attr:
            stdscr.addstr(y, self.WIN_X // 2 - len(text) // 2, text, attr)
        else:
            stdscr.addstr(y, self.WIN_X // 2 - len(text) // 2, text)
        stdscr.refresh()

    def draw(self, stdscr, y, x, my_set):
        stdscr.clear()
        stdscr.addstr(y, x, my_set[0][0], my_set[0][1])
        for chr, color in my_set[1:]:
            stdscr.addstr(chr, color)
        stdscr.refresh()

    def score(self, stdscr, wpm, cpm, accuracy):
        t0 = time.time()
        while True:
            stdscr.clear()
            pct = str(round((accuracy["correct"]/(accuracy["correct"] +
                                                  accuracy["incorrect"]+accuracy["extra"]))*100, 2))+"%"
            self.center_text(
                stdscr, f"WPM: {round((wpm+(cpm/5))/2,2)} / {round((wpm),2)} / {round(cpm/5,2)}", 1*self.WIN_Y//5)
            self.center_text(stdscr, f"CPM: {round(cpm,2)}", 2*self.WIN_Y//5)
            self.center_text(stdscr, f"Accuracy: {pct}", 3*self.WIN_Y//5)
            self.center_text(
                stdscr, f"Correct: {accuracy['correct']}, Incorrect: {accuracy['incorrect']}, Extra: {accuracy['extra']}", 4*self.WIN_Y//5)
            self.center_text(
                stdscr, "Press space to continue", 9*self.WIN_Y//10)
            cur_key = stdscr.getch()
            if cur_key == ord(" ") and (time.time()-t0) >= 1:
                return True
            elif cur_key == 27 or cur_key == curses.KEY_COPY or cur_key == curses.KEY_END or cur_key == curses.KEY_BREAK:
                return False

    def set_colors(self, stdscr):
        if curses.has_colors():
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    def create_set(self):
        pct = 0
        if self.WORD_MODIFICATION == "Weak":
            pct = 0.2
        elif self.WORD_MODIFICATION == "Normal":
            pct = 0.4
        elif self.WORD_MODIFICATION == "Strong":
            pct = 0.6
        elif self.WORD_MODIFICATION == "Extreme":
            pct = 0.8
        elif self.WORD_MODIFICATION == "???":
            pct = 1.0
        raw_set = []
        for _ in range(int(self.WORDS_PER_SET*pct)):
            word = random.choice(self.words)
            method = random.randint(1, 3)
            if method == 1:
                raw_set.append(add_chr(word))
            elif method == 2:
                raw_set.append(delete_chr(word))
            elif method == 3:
                raw_set.append(replace_chr(word))
        raw_set.extend(random.sample(
            self.words, int(self.WORDS_PER_SET*(1-pct))))
        random.shuffle(raw_set)
        return raw_set

    def home(self, stdscr):
        stdscr.clear()
        arrow_x = self.WIN_X // 2 + 10
        arrow_y = 1
        stdscr.addstr(arrow_y*self.WIN_Y//5, arrow_x, "<=")
        stdscr.refresh()
        while True:

            self.center_text(stdscr, "Words", 1*self.WIN_Y//5)
            self.center_text(stdscr, "Time", 2*self.WIN_Y//5)
            self.center_text(stdscr, "Quotes", 3*self.WIN_Y//5)
            self.center_text(stdscr, "Settings", 4*self.WIN_Y//5)
            cur_key = stdscr.getch()
            if cur_key == curses.KEY_DOWN or cur_key == ord('s'):
                arrow_y += 1
                arrow_y %= 5
                if arrow_y == 0:
                    arrow_y = 1
            elif cur_key == curses.KEY_UP or cur_key == ord('w'):
                arrow_y -= 1
                arrow_y %= 5
                if arrow_y == 0:
                    arrow_y = 4
            elif cur_key == 27 or cur_key == curses.KEY_COPY or cur_key == curses.KEY_END or cur_key == curses.KEY_BREAK:  # escape
                return
            elif cur_key == 10 or cur_key == curses.KEY_ENTER:
                if arrow_y == 1:
                    self.practice_set(stdscr)
                elif arrow_y == 2:
                    self.test_set(stdscr)
                elif arrow_y == 4:
                    self.Settings(stdscr)
            stdscr.clear()
            stdscr.addstr(arrow_y*self.WIN_Y//5, arrow_x, "<=")
            stdscr.refresh()
