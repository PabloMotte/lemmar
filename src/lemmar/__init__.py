# __init__.py after edited by you

# from pathlib import Path

import click  # <- click dependency

# from .mywc import mywc
from .lemmar import lemmar_guess, lemmar_status

# @click.command()
# @click.argument("filepath", type=Path)
# @click.option("-c", is_flag=True, help="Show byte count.")
# @click.option("-w", is_flag=True, help="Show word count.")
# @click.option("-l", is_flag=True, help="Show line count.")
# def main(filepath: Path, c: bool | None, w: bool | None, l: bool | None) -> None:
#     """Print newline, word, and byte counts for the given FILEPATH"""
#     # If none of the options was explicitly set, they're all `True`.
#     if {c, w, l} == {False}:
#         c, w, l = True, True, True
#     mywc(filepath, c, w, l)

# @click.argument("file", type=Path)
@click.command()
@click.option("-w5", is_flag=True, help="Words of 5 character length.")
@click.option("-w6", is_flag=True, help="Words of 6 character length.")
@click.option("-w7", is_flag=True, help="Words of 7 character length.")
@click.option("-w8", is_flag=True, help="Words of 8 character length.")
@click.option("-s", is_flag=True, help="Display the current status.")
@click.argument("guess", required=False, help="Guess of current word.")
def main(w5: bool | None, w6: bool | None, w7: bool | None, w8: bool | None, s: bool | None, guess: str | None) -> None:
    """A Wordle-like for the command-line"""
    filepath: str = ""
    guess_len = 0;
    valid_game = True
    if s is None:
        s = False
    if guess is not None:
        guess_len = len(guess);
    # If the length of the guess is valid, override any flags
    match guess_len:
        case 0:
            if {w5, w6, w7, w8} == {False} and s:
                click.echo(lemmar_status())
                valid_game = False
                s = False
        case 5:
            w5, w6, w7, w8 = True, False, False, False
        case 6:
            w5, w6, w7, w8 = False, True, False, False
        case 7:
            w5, w6, w7, w8 = False, False, True, False
        case 8:
            w5, w6, w7, w8 = False, False, False, True
    # If none of the options was explicitly set, the -w5 option is `True`.
    if {w5, w6, w7, w8} == {False}:
        w5, w6, w7, w8 = True, False, False, False
    else:
        # Make sure we have a valid game request
        match guess_len:
            case 0:
                # Probably starting a new game
                pass
            case 5:
                if {w6, w7, w8} != {False}:
                    click.echo("Invalid guess length")
                    valid_game = False
            case 6:
                if {w5, w7, w8} != {False}:
                    click.echo("Invalid guess length")
                    valid_game = False
            case 7:
                if {w5, w6, w8} != {False}:
                    click.echo("Invalid guess length")
                    valid_game = False
            case 8:
                if {w5, w6, w7} != {False}:
                    click.echo("Invalid guess length")
                    valid_game = False
            case _:
                click.echo("Invalid guess length")
                valid_game = False
    if valid_game:
        if w5:
            filepath = "WORDS_5.txt"
        if w6:
            filepath = "WORDS_6.txt"
        if w7:
            filepath = "WORDS_7.txt"
        if w8:
            filepath = "WORDS_8.txt"
        # click.echo(f"File: {filepath}")
        # click.echo(f"Guess: {guess}")
        click.echo(lemmar_guess(filepath, guess))
    elif not valid_game and s:
        click.echo(lemmar_status())

