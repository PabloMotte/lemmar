# __init__.py after edited by you

from pathlib import Path

import click  # <- click dependency

from .mywc import mywc


@click.command()
@click.argument("filepath", type=Path)
@click.option("-c", is_flag=True, help="Show byte count.")
@click.option("-w", is_flag=True, help="Show word count.")
@click.option("-l", is_flag=True, help="Show line count.")
def main(filepath: Path, c: bool | None, w: bool | None, l: bool | None) -> None:
    """Print newline, word, and byte counts for the given FILEPATH"""
    # If none of the options was explicitly set, they're all `True`.
    if {c, w, l} == {False}:
        c, w, l = True, True, True
    mywc(filepath, c, w, l)
