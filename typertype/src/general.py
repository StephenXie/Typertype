from .words_mode import Typer_words
from .time_mode import Typer_time
from .quotes_mode import Typer_quotes


class Typer(Typer_words,Typer_time, Typer_quotes):
    pass