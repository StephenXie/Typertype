import os
import json

here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, 'list_of_words.txt')
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

def get_settings():
    return settings