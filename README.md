# Lemmar

A Wordle-like, run from the command-line.


## Wordle's Core Rules

- Guess a valid word: Every guess must be a real 5-letter English word recognized by the game's dictionary.
- Color-coded feedback: After each guess, the tile colors change to give you clues:
- - Green: The letter is in the word and in the correct position.
- - Yellow: The letter is in the word, but in the wrong position.
- - Gray: The letter is not in the word at all.
- Six tries limit: You have 6 total rows to find the solution before the game ends.

## Special Rules & Edge Cases

- Double letters: If the secret word has a repeated letter (like "SPEED") and you guess a word with too many of that letter (like "GEESE"), only the first instances light up; extra instances turn gray.
- Green priority: Green matches are locked in first before any yellow matches are assigned.
- Hard Mode: An optional setting in the menu that forces you to reuse any revealed green and yellow letters in your subsequent guesses

## Lemmar rules

- Will be mostly the same, but allow user to select a game of 5, 6, 7 or 8 letters. Each higher letter count gives an additional try.
- Colours are unlikely to be used:
- - ^A^: The letter is in the word and in the correct position.
- - \<A\>: The letter is in the word, but in the wrong position.
- - .A.: The letter is not in the word at all.

_Clone and Run instructions to follow..._

## Cloning the repository

Click the Code drop-down above-right of the file list, where all the cloning instructions you could ever want are available.

For those not willing to work it out, make sure git is installed by typing ```git -v``` on the command line, then navigate to some "projects" folder and type ```git clone https://github.com/PabloMotte/lemmar.git lemmar```

All pull requests will be denied until I am happy to start sharing with everyone else. (The project is "public" because that was demanded by my tutors at [boot.dev](https:\\boot.dev).)
