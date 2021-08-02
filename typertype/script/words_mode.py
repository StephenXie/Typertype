from main import *

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