# Typertype
Typertype is an offline, customizable, feature-rich, typing app. It allows users to practice typing and test their typing speed offline with a wide array of customizability. It
analyzes the user's typing data and outputs information such as WPM, CPM, and accuracy. Users can modify settings
to better fit their preferences and help provide a better typing experience such as correction mechanism, word
modification, etc.

## Features
Typertype currently have the following modes: Word, Time, Quotes(coming soon)
Typertype is able to...

- save your typing preference by storing them in JSON format locally
- modify words by randomly swapping, adding, or removing letters in words to help you adapt to different typing scenarios.
- allow users to correct their words in different ways such as
  - stopping the cursor if a letter is typed wrong
  - moving on and skipping the letters typed wrong but allowing backspacing to fix the wrong letters
  - skipping the letters typed wrong but doesn't allow backspacing
- analyze typing data and give statistics
- and much more!


## Installation
```
pip install typertype
```
Note that if you are using windows, you will have to install the curses library seperately using the following
```
pip install windows-curses
```

## Usage
Import typertype by using
```python
import typertype
```
You can start typing by creating a python(.py) script such as
```python
import typertype

tt = typertype.Typertype()

tt.run()
```

That's it! No additional steps are required to run the program.

