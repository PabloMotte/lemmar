import linecache
import os
import re
import sys
from random import randrange

from config import DATA_DIR

CHUNK_SIZE = 4096


def bufcount(filename):
    lines = 0
    with open(filename) as f:
        buf_size = CHUNK_SIZE
        read_f = f.read # loop optimization

        buf = read_f(buf_size)
        while buf:
            lines += buf.count('\n')
            buf = read_f(buf_size)

    return lines

def lemmar(filename: str = "WORDS_5.txt") -> tuple[str, str] | None:
    try:
        full_filename = os.path.join(DATA_DIR, filename)
        line_count = bufcount(full_filename)
        if line_count > 0:
            content: str = ""
            count_blanks: int = 0
            while content == "" and count_blanks < 3:
                chosen_Line = randrange(1, line_count)
                content = linecache.getline(full_filename, chosen_Line)
                content = content.strip().upper()
                print(f"Found: |{content}|")
                if re.fullmatch("^[A-Z]+", content) is None:
                    content = ""
                if content == "":
                    count_blanks += 1
            if content == "" or count_blanks >= 3:
                return (f"Failed: {count_blanks}, {filename}, {line_count}", "")
            else:
                return (f"Found: {content}, {filename}, {line_count}"
                    , f"https://en.wiktionary.org/wiki/{content}")
    except FileNotFoundError as e:
        return (f"Error: FileNotFoundError, {e}", "")
    return None

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "":
        print(lemmar(sys.argv[1]))
    else:
        print(lemmar())
