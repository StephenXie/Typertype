import random
import curses
import time
from .main import Typer_base

class Typer_time(Typer_base):
    def test_set(self,stdscr):
        started = False
        l, r = 0, self.WIN_X-self.X-1
        accuracy = {"correct": 0, "incorrect": 0, "extra": 0}
        stdscr.clear()
        raw_set = random.sample(self.words, len(self.words))
        chr_set = list(" ".join(raw_set))
        cur_set = [[chr, curses.color_pair(1)] for chr in chr_set]
        timer_x, timer_y = 2, 2
        self.draw(stdscr, self.Y, self.X, cur_set[l:r+1])
        i = 0
        stdscr.addstr(timer_y, timer_x, str(round(self.TEST_TIMER, 2)))
        stdscr.refresh()
        while i < len(cur_set):
            if started:
                stdscr.addstr(timer_y, timer_x, str(
                    round(self.TEST_TIMER-(time.time()-t0), 2)))
                stdscr.refresh()
            cur_key = stdscr.getch()
            if not started:
                started = True
                t0 = time.time()
            if time.time()-t0 >= self.TEST_TIMER:
                break
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
                    if i >= self.WIN_X//2:
                        l -= 1
                        r -= 1
                    i -= 1

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
        cpm = accuracy["correct"]*(60/self.TEST_TIMER)
        wpm = len(" ".join(raw_set)[:i+1].split())*(60/self.TEST_TIMER)
        if self.score(stdscr, wpm, cpm, accuracy):
            self.test_set(stdscr)
        else:
            return