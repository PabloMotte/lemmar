# Lemmar

A Wordle-like, run from the command-line.

## Lemmar Usage

```text
Usage: lemmar [OPTIONS] [GUESS]

  A Wordle-like for the command-line

Positional arguments:
  [GUESS]  Guess of current word.

Options:
  -w5     Words of 5 character length.
  -w6     Words of 6 character length.
  -w7     Words of 7 character length.
  -w8     Words of 8 character length.
  -s      Display the current status.
  --help  Show this message and exit.
```

## Lemmar rules

- Will be mostly the same as Wordle's, but allow user to select a game of 5, 6, 7 or 8 letters - either by selecting the option, or by providing the correct number of letters in the guess. Each higher letter count gives an additional try.
- Colours are unlikely to be used, because I am colour-blind:
- - ^A^: The letter is in the word and in the correct position.
- - \<A\>: The letter is in the word, but in the wrong position.
- - .A.: The letter is not in the word at all.

### Wordle's Core Rules

- Guess a valid word: Every guess must be a real 5-letter English word recognized by the game's dictionary.
- Color-coded feedback: After each guess, the tile colors change to give you clues:
- - Green: The letter is in the word and in the correct position.
- - Yellow: The letter is in the word, but in the wrong position.
- - Gray: The letter is not in the word at all.
- Six tries limit: You have 6 total rows to find the solution before the game ends.

### Wordle Special Rules & Edge Cases

- Double letters: If the secret word has a repeated letter (like "SPEED") and you guess a word with too many of that letter (like "GEESE"), only the first instances light up; extra instances turn gray.
- Green priority: Green matches are locked in first before any yellow matches are assigned.
- Hard Mode: An optional setting in the menu that forces you to reuse any revealed green and yellow letters in your subsequent guesses

## Cloning the repository

_Clone and Run instructions to be amended..._

### Cloning

Click the Code drop-down above-right of the file list in [GitHub](https://github.com), where all the cloning instructions you could ever want are available.

For those not willing to work it out, make sure git is installed by typing `git -v` on the command line, then navigate to some "projects" folder and type `git clone https://github.com/PabloMotte/lemmar.git lemmar`

### Running

Once cloned, you can run the package from the folder with uv (assuming you have [uv installed](https://docs.astral.sh/uv/#installation)):

- `uv run lemmar`

or, you can install as the `lemmar` command in unix-based systems

- `uv tool install . -e`

### Pull Requests

All pull requests will be denied until I am happy to start sharing with everyone else. (The project is "public" because that was demanded by my tutors at [boot.dev](https:\\boot.dev).)
