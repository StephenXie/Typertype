from main import *
from words_mode import *

def home(stdscr):
    stdscr.clear()
    arrow_x = WIN_X // 2 + 10
    arrow_y = 1
    stdscr.addstr(arrow_y*WIN_Y//4, arrow_x, "<=")
    stdscr.refresh()
    while True:

        center_text(stdscr, "Words", 1*WIN_Y//5)
        center_text(stdscr, "Time", 2*WIN_Y//5)
        center_text(stdscr, "Quotes", 3*WIN_Y//5)
        center_text(stdscr, "Settings", 4*WIN_Y//5)
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
                arrow_y = 3
        elif cur_key == 27 or cur_key == curses.KEY_COPY or cur_key == curses.KEY_END or cur_key == curses.KEY_BREAK:  # escape
            return
        elif cur_key == 10 or cur_key == curses.KEY_ENTER:
            if arrow_y == 1:
                practice_set(stdscr)
            elif arrow_y == 2:
                test_set(stdscr)
            elif arrow_y == 4:
                Settings(stdscr)
        stdscr.clear()
        stdscr.addstr(arrow_y*WIN_Y//5, arrow_x, "<=")
        stdscr.refresh()


def start(stdscr):
    global WIN_X
    global WIN_Y
    WIN_Y, WIN_X = stdscr.getmaxyx()
    global X
    global Y
    Y = WIN_Y // 2
    set_colors(stdscr)
    curses.curs_set(False)
    home(stdscr)

def main():
    
    setup()
    curses.wrapper(start)
    with open("settings.json", "w") as settings_file:
        json.dump(settings, settings_file, indent=4)

    
main()