import random

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
