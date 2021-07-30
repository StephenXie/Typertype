import curses
import random
import time
import json
# Credits to Curses python library and https://docs.python.org/3/howto/curses.html for basic command line interface control.
# Credits to JSON python library and https://docs.python.org/3/library/json.html for reading and writing JSON files.
try:
    with open("settings.json") as settings_file:
        settings = json.load(settings_file)
except FileNotFoundError:  # no current settings exist(i.e. file is empty)
    settings = {
        "WORDS_PER_SET": 20,
        "CORRECTIONS": "None",
        "TEST_TIMER": 60,
        "SPACE_STOP": True,
        "WORD_MODIFICATION": "Normal"
    }
WORDS_PER_SET = settings.get("WORDS_PER_SET", 20)
CORRECTIONS = settings.get("CORRECTIONS", "None")
TEST_TIMER = settings.get("TEST_TIMER", 60)
SPACE_STOP = settings.get("SPACE_STOP", True)
WORD_MODIFICATION = settings.get("WORD_MODIFICATION", "Normal")
Y, X = 5, 5
WIN_X, WIN_Y = 0, 0
words = []
# The text file contains a list of common English words
with open("list_of_words.txt", "r") as reader:
    for line in reader:
        words.append(line.replace("\n", ""))


def Settings(stdscr):
    global WORDS_PER_SET
    global CORRECTIONS
    global SPACE_STOP
    global TEST_TIMER
    global SPACE_STOP
    global WORD_MODIFICATION
    stdscr.clear()
    arrow_x = WIN_X // 2 + 12
    arrow_y = 1
    stdscr.refresh()
    while True:
        center_text(stdscr, "Settings", WIN_Y//12)
        center_text(stdscr, f"Words Per Set: {WORDS_PER_SET} words", WIN_Y//6)
        center_text(stdscr, f"Corrections: {CORRECTIONS}", 2*WIN_Y//6)
        center_text(stdscr, f"Test Timer: {TEST_TIMER} seconds", 3*WIN_Y//6)
        center_text(stdscr, f"Space Stop: {SPACE_STOP}", 4*WIN_Y//6)
        center_text(
            stdscr, f"Word Modification: {WORD_MODIFICATION}", 5*WIN_Y//6)
        if arrow_y == 1:
            cur_key, WORDS_PER_SET = set_option(stdscr, "Words per set", [
                5, 10, 15, 20, 25, 30, 35, 40, 45, 50], WIN_Y//6, WORDS_PER_SET, "words")
        elif arrow_y == 2:
            cur_key, CORRECTIONS = set_option(
                stdscr, "Corrections", ["None", "Backspace", "Stop"], 2*WIN_Y//6, CORRECTIONS)
        elif arrow_y == 3:
            cur_key, TEST_TIMER = set_option(stdscr, "Test timer", [
                10, 15, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300], 3*WIN_Y//6, TEST_TIMER, "seconds")
        elif arrow_y == 4:
            cur_key, SPACE_STOP = set_option(
                stdscr, "Space stop", [True, False], 4*WIN_Y//6, SPACE_STOP)
        elif arrow_y == 5:
            cur_key, WORD_MODIFICATION = set_option(stdscr, "Word modification", [
                "None", "Weak", "Normal", "Strong", "Extreme", "???"], 5*WIN_Y//6, WORD_MODIFICATION)
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


def set_option(stdscr, name, options, y, cur, message=""):
    global settings
    i = options.index(cur)
    var_name = name.replace(" ", "_").upper()
    if message != "":
        center_text(stdscr, f"< {name.title()}: {options[i]} {message} >", y)
    else:
        center_text(stdscr, f"< {name.title()}: {options[i]} >", y)
    cur_key = stdscr.getch()
    while True:
        clr_cur_line(stdscr, y)
        if cur_key == curses.KEY_LEFT or cur_key == ord("a"):
            i -= 1
            i = i % len(options)
        elif cur_key == curses.KEY_RIGHT or cur_key == ord("d"):
            i += 1
            i = i % len(options)
        else:
            return cur_key, settings[var_name]
        if message:
            center_text(
                stdscr, f"< {name.title()}: {options[i]} {message} >", y)
        else:
            center_text(stdscr, f"< {name.title()}: {options[i]} >", y)
        settings[var_name] = options[i]
        cur_key = stdscr.getch()


def clr_cur_line(stdscr, y):
    stdscr.addstr(y, 0, " "*WIN_X)
    stdscr.refresh()


def center_text(stdscr, text, y=WIN_Y // 2, attr=None):
    if attr:
        stdscr.addstr(y, WIN_X // 2 - len(text) // 2, text, attr)
    else:
        stdscr.addstr(y, WIN_X // 2 - len(text) // 2, text)
    stdscr.refresh()


def practice_set(stdscr):
    started = False
    l, r = 0, WIN_X-X-1
    accuracy = {"correct": 0, "incorrect": 0, "extra": 0}
    stdscr.clear()
    raw_set = create_set()
    chr_set = list(" ".join(raw_set))
    cur_set = [[chr, curses.color_pair(1)] for chr in chr_set]
    draw(stdscr, Y, X, cur_set[l:r+1])
    i = 0
    while i < len(cur_set):
        cur_key = stdscr.getch()
        if not started:
            started = True
            t0 = time.time()
        if cur_key == ord(chr_set[i]):
            if CORRECTIONS == "Stop":
                if cur_set[i][1] == curses.color_pair(2) | curses.A_BLINK:
                    cur_set[i][1] = curses.color_pair(2)
                else:
                    cur_set[i][1] = curses.color_pair(3)
            else:
                cur_set[i][1] = curses.color_pair(3)

            if i < len(cur_set)-1:
                cur_set[i+1][1] = curses.color_pair(1) | curses.A_BLINK

            i += 1
            if i >= WIN_X//2:
                l += 1
                r += 1
            accuracy["correct"] += 1
        elif cur_key == 27 or cur_key == curses.KEY_COPY or cur_key == curses.KEY_END or cur_key == curses.KEY_BREAK:
            return
        # backspace:
        elif cur_key == 8 or cur_key == curses.KEY_BACKSPACE:
            if cur_set[i-1][1] == curses.color_pair(2) and CORRECTIONS == "Backspace":
                cur_set[i][1] = curses.color_pair(1)
                cur_set[i-1][1] = curses.color_pair(2) | curses.A_BLINK
                i -= 1
                if i >= WIN_X//2:
                    l -= 1
                    r -= 1
        elif not(SPACE_STOP and cur_key == ord(" ")):
            cur_set[i][1] = curses.color_pair(2)
            if CORRECTIONS == "Stop":
                cur_set[i][1] = curses.color_pair(2) | curses.A_BLINK
            if i < len(cur_set)-1 and CORRECTIONS != "Stop":
                cur_set[i+1][1] = curses.color_pair(1) | curses.A_BLINK
            if chr_set[i] == " ":
                accuracy["extra"] += 1
            else:
                accuracy["incorrect"] += 1
            if CORRECTIONS == "None" or CORRECTIONS == "Backspace":
                i += 1
                if i >= WIN_X//2:
                    l += 1
                    r += 1
        draw(stdscr, Y, X, cur_set[l:r+1])
    t1 = time.time()
    my_time = t1-t0
    cpm = accuracy["correct"]*(60/my_time)
    wpm = WORDS_PER_SET*(60/my_time)
    if score(stdscr, wpm, cpm, accuracy):
        practice_set(stdscr)
    else:
        return


def test_set(stdscr):
    started = False
    l, r = 0, WIN_X-X-1
    accuracy = {"correct": 0, "incorrect": 0, "extra": 0}
    stdscr.clear()
    raw_set = random.sample(words, len(words))
    chr_set = list(" ".join(raw_set))
    cur_set = [[chr, curses.color_pair(1)] for chr in chr_set]
    timer_x, timer_y = 2, 2
    draw(stdscr, Y, X, cur_set[l:r+1])
    i = 0
    stdscr.addstr(timer_y, timer_x, str(round(TEST_TIMER, 2)))
    stdscr.refresh()
    while i < len(cur_set):
        if started:
            stdscr.addstr(timer_y, timer_x, str(
                round(TEST_TIMER-(time.time()-t0), 2)))
            stdscr.refresh()
        cur_key = stdscr.getch()
        if not started:
            started = True
            t0 = time.time()
        if time.time()-t0 >= TEST_TIMER:
            break
        if cur_key == ord(chr_set[i]):
            if CORRECTIONS == "Stop":
                if cur_set[i][1] == curses.color_pair(2) | curses.A_BLINK:
                    cur_set[i][1] = curses.color_pair(2)
                else:
                    cur_set[i][1] = curses.color_pair(3)
            else:
                cur_set[i][1] = curses.color_pair(3)

            if i < len(cur_set)-1:
                cur_set[i+1][1] = curses.color_pair(1) | curses.A_BLINK

            i += 1
            if i >= WIN_X//2:
                l += 1
                r += 1
            accuracy["correct"] += 1
        elif cur_key == 27 or cur_key == curses.KEY_COPY or cur_key == curses.KEY_END or cur_key == curses.KEY_BREAK:
            return
        # backspace:
        elif cur_key == 8 or cur_key == curses.KEY_BACKSPACE:
            if cur_set[i-1][1] == curses.color_pair(2) and CORRECTIONS == "Backspace":
                cur_set[i][1] = curses.color_pair(1)
                cur_set[i-1][1] = curses.color_pair(2) | curses.A_BLINK
                if i >= WIN_X//2:
                    l -= 1
                    r -= 1
                i -= 1

        elif not(SPACE_STOP and cur_key == ord(" ")):
            cur_set[i][1] = curses.color_pair(2)
            if CORRECTIONS == "Stop":
                cur_set[i][1] = curses.color_pair(2) | curses.A_BLINK
            if i < len(cur_set)-1 and CORRECTIONS != "Stop":
                cur_set[i+1][1] = curses.color_pair(1) | curses.A_BLINK
            if chr_set[i] == " ":
                accuracy["extra"] += 1
            else:
                accuracy["incorrect"] += 1
            if CORRECTIONS == "None" or CORRECTIONS == "Backspace":
                i += 1
                if i >= WIN_X//2:
                    l += 1
                    r += 1
        draw(stdscr, Y, X, cur_set[l:r+1])
    cpm = accuracy["correct"]*(60/TEST_TIMER)
    wpm = len(" ".join(raw_set)[:i+1].split())*(60/TEST_TIMER)
    if score(stdscr, wpm, cpm, accuracy):
        test_set(stdscr)
    else:
        return


def draw(stdscr, y, x, my_set):
    stdscr.clear()
    stdscr.addstr(y, x, my_set[0][0], my_set[0][1])
    for chr, color in my_set[1:]:
        stdscr.addstr(chr, color)
    stdscr.refresh()


def score(stdscr, wpm, cpm, accuracy):
    t0 = time.time()
    while True:
        stdscr.clear()
        pct = str(round((accuracy["correct"]/(accuracy["correct"] +
                                              accuracy["incorrect"]+accuracy["extra"]))*100, 2))+"%"
        center_text(
            stdscr, f"WPM: {round((wpm+(cpm/5))/2,2)} / {round((wpm),2)} / {round(cpm/5,2)}", 1*WIN_Y//5)
        center_text(stdscr, f"CPM: {round(cpm,2)}", 2*WIN_Y//5)
        center_text(stdscr, f"Accuracy: {pct}", 3*WIN_Y//5)
        center_text(
            stdscr, f"Correct: {accuracy['correct']}, Incorrect: {accuracy['incorrect']}, Extra: {accuracy['extra']}", 4*WIN_Y//5)
        center_text(stdscr, "Press space to continue", 9*WIN_Y//10)
        cur_key = stdscr.getch()
        if cur_key == ord(" ") and (time.time()-t0) >= 1:
            return True
        elif cur_key == 27 or cur_key == curses.KEY_COPY or cur_key == curses.KEY_END or cur_key == curses.KEY_BREAK:
            return False


def home(stdscr):
    stdscr.clear()
    arrow_x = WIN_X // 2 + 10
    arrow_y = 1
    stdscr.addstr(arrow_y*WIN_Y//4, arrow_x, "<=")
    stdscr.refresh()
    while True:

        center_text(stdscr, "Practice", 1*WIN_Y//4)
        center_text(stdscr, "Test", 2*WIN_Y//4)
        center_text(stdscr, "Settings", 3*WIN_Y//4)
        cur_key = stdscr.getch()
        if cur_key == curses.KEY_DOWN or cur_key == ord('s'):
            arrow_y += 1
            arrow_y %= 4
            if arrow_y == 0:
                arrow_y = 1
        elif cur_key == curses.KEY_UP or cur_key == ord('w'):
            arrow_y -= 1
            arrow_y %= 4
            if arrow_y == 0:
                arrow_y = 3
        elif cur_key == 27 or cur_key == curses.KEY_COPY or cur_key == curses.KEY_END or cur_key == curses.KEY_BREAK:  # escape
            return
        elif cur_key == 10 or cur_key == curses.KEY_ENTER:
            if arrow_y == 1:
                practice_set(stdscr)
            elif arrow_y == 2:
                test_set(stdscr)
            elif arrow_y == 3:
                Settings(stdscr)
        stdscr.clear()
        stdscr.addstr(arrow_y*WIN_Y//4, arrow_x, "<=")
        stdscr.refresh()


def set_colors(stdscr):
    if curses.has_colors():
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)


def create_set():
    pct = 0
    if WORD_MODIFICATION == "Weak":
        pct = 0.2
    elif WORD_MODIFICATION == "Normal":
        pct = 0.4
    elif WORD_MODIFICATION == "Strong":
        pct = 0.6
    elif WORD_MODIFICATION == "Extreme":
        pct = 0.8
    elif WORD_MODIFICATION == "???":
        pct = 1.0
    raw_set = []
    for _ in range(int(WORDS_PER_SET*pct)):
        word = random.choice(words)
        method = random.randint(1, 3)
        if method == 1:
            raw_set.append(add_chr(word))
        elif method == 2:
            raw_set.append(delete_chr(word))
        elif method == 3:
            raw_set.append(replace_chr(word))
    raw_set.extend(random.sample(words, int(WORDS_PER_SET*(1-pct))))
    random.shuffle(raw_set)
    return raw_set


def add_chr(word):
    word = list(word)
    word.insert(random.randint(0, len(word)), chr(
        random.randint(ord("a"), ord("z"))))
    return "".join(word)


def delete_chr(word):
    word = list(word)
    word.pop(random.randint(0, len(word)-1))
    return "".join(word)


def replace_chr(word):
    word = list(word)
    word[random.randint(0, len(word)-1)
         ] = chr(random.randint(ord("a"), ord("z")))
    return "".join(word)


def main(stdscr):
    global WIN_X
    global WIN_Y
    WIN_Y, WIN_X = stdscr.getmaxyx()
    global X
    global Y
    Y = WIN_Y // 2
    set_colors(stdscr)
    curses.curs_set(False)
    home(stdscr)


curses.wrapper(main)
with open("settings.json", "w") as settings_file:
    json.dump(settings, settings_file, indent=4)
