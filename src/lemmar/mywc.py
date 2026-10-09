from pathlib import Path


def mywc(filepath: Path, show_bytes: bool, show_words: bool, show_lines: bool) -> None:
    """Print newline, word, and byte counts for the given FILEPATH"""
    content = filepath.read_bytes()
    byte_count = len(content)
    word_count = len(content.split())
    line_count = len(content.splitlines())
    output = ("wc: " +
        (f"{line_count:8}" if show_lines else "")
        + (f"{word_count:8}" if show_words else "")
        + (f"{byte_count:8}" if show_bytes else "")
        + f" {filepath}"
    )
    print(output)

if __name__ == "__main__":
    mywc(Path(__file__), True, True, True)
