# Typertype

[![PyPI version fury.io](https://badge.fury.io/py/typertype.svg)](https://pypi.python.org/pypi/typertype/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![GitHub issues](https://img.shields.io/github/issues/StephenXie/Typertype)](https://GitHub.com/StephenXie/Typertype/issues/) [![GitHub issues](https://img.shields.io/github/issues-closed/StephenXie/Typertype)](https://github.com/StephenXie/Typertype/issues?q=is%3Aissue+is%3Aclosed)
***
Typertype is an offline, customizable, feature-rich, typing app. It allows users to practice typing habits and test their typing speed offline with a wide array of customizability.
<!-- 
## IMPORTANT

Due to the possibility of some restrictions from collegeboard(AP CSP Create Performance Task), the project's publish date will be delayed to June 2022.
 -->
## Installation

```bash
pip install typertype
```

Note that if you are using windows, you will have to install the curses library seperately using the following

```bash
pip install windows-curses
```

## Usage

Import typertype by using

```python
import typertype
```

You can start typing by creating a python(.py) script or by simply opening up a python shell

```python
>> import typertype

>> tt = typertype.Typertype()

>> tt.run()
```

That's it! You can run the commands and start typing even without internet, and your settings will be automatically saved each time. No additional steps are required to run the program.

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
- and much much more!

## Demo

![Demo](https://stephenxie.github.io/images/ezgif.com-gif-maker.gif)
