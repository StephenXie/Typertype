import curses
import json
from .src.general import Typer
# Copyright (c) 2021 Pin Xie. All rights reserved. Use of this source code is governed by GNU GPLv3 license that can be found in the LICENSE file.

class Typertype:
    def __init__(self):
        pass

    def start(self, stdscr):
        self.typer = Typer(stdscr)
        self.typer.home(stdscr)

    def run(self):
        curses.wrapper(self.start)
        with open("settings.json", "w") as settings_file:
            json.dump(self.typer.settings, settings_file, indent=4)
