from . import words_mode
from . import time_mode
from . import quotes_mode


class Typer(words_mode.Typer_words,time_mode.Typer_time, quotes_mode.Typer_quotes):
    pass