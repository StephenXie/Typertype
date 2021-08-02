import random
import curses
import time
from .main import Typer_base

class Typer_words(Typer_base):
    def practice_set(self,stdscr):
        started = False
        l, r = 0, self.WIN_X-self.X-1
        accuracy = {"correct": 0, "incorrect": 0, "extra": 0}
        stdscr.clear()
        raw_set = self.create_set()
        chr_set = list(" ".join(raw_set))
        cur_set = [[chr, curses.color_pair(1)] for chr in chr_set]
        self.draw(stdscr, self.Y, self.X, cur_set[l:r+1])
        i = 0
        while i < len(cur_set):
            cur_key = stdscr.getch()
            if not started:
                started = True
                t0 = time.time()
            if cur_key == ord(chr_set[i]):
                if self.CORRECTIONS == "Stop":
                    if cur_set[i][1] == curses.color_pair(2) | curses.A_BLINK:
                        cur_set[i][1] = curses.color_pair(2)
                    else:
                        cur_set[i][1] = curses.color_pair(3)
                else:
                    cur_set[i][1] = curses.color_pair(3)

                if i < len(cur_set)-1:
                    cur_set[i+1][1] = curses.color_pair(1) | curses.A_BLINK

                i += 1
                if i >= self.WIN_X//2:
                    l += 1
                    r += 1
                accuracy["correct"] += 1
            elif cur_key == 27 or cur_key == curses.KEY_COPY or cur_key == curses.KEY_END or cur_key == curses.KEY_BREAK:
                return
            # backspace:
            elif cur_key == 8 or cur_key == curses.KEY_BACKSPACE:
                if cur_set[i-1][1] == curses.color_pair(2) and self.CORRECTIONS == "Backspace":
                    cur_set[i][1] = curses.color_pair(1)
                    cur_set[i-1][1] = curses.color_pair(2) | curses.A_BLINK
                    i -= 1
                    if i >= self.WIN_X//2:
                        l -= 1
                        r -= 1
            elif not(self.SPACE_STOP and cur_key == ord(" ")):
                cur_set[i][1] = curses.color_pair(2)
                if self.CORRECTIONS == "Stop":
                    cur_set[i][1] = curses.color_pair(2) | curses.A_BLINK
                if i < len(cur_set)-1 and self.CORRECTIONS != "Stop":
                    cur_set[i+1][1] = curses.color_pair(1) | curses.A_BLINK
                if chr_set[i] == " ":
                    accuracy["extra"] += 1
                else:
                    accuracy["incorrect"] += 1
                if self.CORRECTIONS == "None" or self.CORRECTIONS == "Backspace":
                    i += 1
                    if i >= self.WIN_X//2:
                        l += 1
                        r += 1
            self.draw(stdscr, self.Y, self.X, cur_set[l:r+1])
        t1 = time.time()
        my_time = t1-t0
        cpm = accuracy["correct"]*(60/my_time)
        wpm = self.WORDS_PER_SET*(60/my_time)
        if self.score(stdscr, wpm, cpm, accuracy):
            self.practice_set(stdscr)
        else:
            return