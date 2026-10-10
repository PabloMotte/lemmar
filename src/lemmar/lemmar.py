import hashlib
import json
import linecache
import os
import re
import sys
from pathlib import Path
from random import randrange
from typing import Any

from config import GAME_DATA_DIR, WORD_DATA_DIR

CHUNK_SIZE = 4096
# Keys for the dictionary
LEMMAR_DICT_IDX = "chosen_line"
LEMMAR_DICT_STS = "status"
LEMMAR_DICT_DONE = "done"
LEMMAR_DICT_WON = "won"
LEMMAR_IDX = 0
LEMMAR_STS = 1
LEMMAR_DONE = 2
LEMMAR_WON = 3


def bufcount(filename):
    lines = 0
    full_filename = os.path.join(WORD_DATA_DIR, filename)
    if Path(full_filename).exists():
        with open(full_filename) as f:
            buf_size = CHUNK_SIZE
            read_f = f.read # loop optimization

            buf = read_f(buf_size)
            while buf:
                lines += buf.count('\n')
                buf = read_f(buf_size)

    return lines

def amend_string(input: str, index: int, insert: str = " ") -> str:
    """return a string with the character at position index changed to insert"""
    if index < 0 or index >= len(input):
        return input
    output = input[:index] + insert + input[index+1:]
    # print(f"in: {input}, pre: {input[:index]}, post: {input[index+1:]}")
    return output

def lemmar_guess(filename: str, guess: str) -> str:
    if guess is None:
        new_guess = ""
    else:
        new_guess = guess.strip().upper()
    game_result = ""
    saved_results = lemmar_load(filename)
    if saved_results[LEMMAR_IDX] < 0 or saved_results[LEMMAR_DONE]:
        new_game = lemmar_new(filename)
        if new_game is None:
            raise ValueError("Unable to choose new word")
        saved_results = (new_game[2], [], False, False)
        game_result = "== new game\n"
    check_word = get_word(filename, saved_results[LEMMAR_IDX])
    if len(new_guess) == 0:
        pass
    elif len(check_word) == len(new_guess):
        count_good, count_bad, count_misplaced = 0, 0, 0
        list_good, list_misplaced = [], []
        track_word = check_word
        track_guess = new_guess
        # Remove exact match and no match from track_word
        for i in range(len(new_guess)):
            if new_guess[i] == check_word[i]:
                # Green result, but no colours yet
                # Remove matching letter from track_word and track_guess
                track_word = amend_string(track_word, i)
                track_guess = amend_string(track_guess, i)
                list_good.append(new_guess[i])
            else:
                list_good.append(" ")
        # Find misplaced letters in altered word, using altered guess value
        for i in range(len(track_guess)):
            if track_guess[i] == " ":
                # We've already fixed this guessed letter in place
                list_misplaced.append(" ")
            elif track_guess[i] in track_word:
                # Yellow result, but no colours yet
                list_misplaced.append(track_guess[i])
                # Remove the found misplaced letter once from track_word
                idx = track_word.find(track_guess[i])
                if idx > -1:
                    track_word = amend_string(track_word, idx)
            else:
                list_misplaced.append(" ")
        for i in range(len(new_guess)):
            if new_guess[i] == list_good[i]:
                game_result += f"^{new_guess[i]}^"
                count_good += 1
            elif new_guess[i] == list_misplaced[i]:
                game_result += f"<{new_guess[i]}>"
                count_misplaced += 1
            else:
                game_result += f".{new_guess[i]}."
                count_bad += 1
        # print("good: ", "".join(list_good))
        # print("misplaced: ", "".join(list_misplaced))
        saved_list = saved_results[LEMMAR_STS]
        saved_list.append(game_result)
        done = saved_results[LEMMAR_DONE]
        won = saved_results[LEMMAR_WON]
        # Game over conditions
        if (len(saved_list) > len(check_word)
                or count_good == len(check_word)):
            if count_good == len(check_word):
                won = True
            done = True
        lemmar_save(filename, saved_results[LEMMAR_IDX], saved_list, done, won)
        game_result += f" == {count_good} good, {count_misplaced} misplaced, {count_bad} bad"

        # Game over condition results
        if done and won:
            game_result += " \n== You won!"
        elif done and not won:
            game_result += f" \n== You failed! The word was {check_word}."
    else:
        game_result = f"== invalid guess: {new_guess}=="
    if game_result.startswith("== "):
        game_result += f" \n== guess the {len(check_word)} letters"

    return game_result

def lemmar_status() -> str:
    game_results: list[str] = []
    files = [5, 6, 7, 8]
    for file in files:
        result = ""
        filename = f"WORDS_{file}.txt"
        saved_results = lemmar_load(filename)
        if saved_results[LEMMAR_DONE]:
            # This game is complete
            if len(saved_results[LEMMAR_STS]) > 0 and saved_results[LEMMAR_WON]:
                result = f"Correctly Guessed *{file}* word = {saved_results[LEMMAR_STS][-1]}"
            elif len(saved_results[LEMMAR_STS]) > 0 and not saved_results[LEMMAR_WON]:
                result = f"Failed to Guess the *{file}* word"
            elif len(saved_results[LEMMAR_STS]) == 0:
                result = f"Haven't played for *{file}* word"
        else:
            # This game is complete
            if len(saved_results[LEMMAR_STS]) > 0:
                result = f"Haven't Guessed *{file}* word yet. Last try = {saved_results[LEMMAR_STS][-1]}"
            elif len(saved_results[LEMMAR_STS]) == 0:
                result = f"Haven't made a guess for *{file}* word"
        game_results.append(result)
    all_game_results = ""
    for result in game_results:
        all_game_results += (("\n" if len(all_game_results) > 0 else "") + result)

    return all_game_results

def dict_hash(dictionary: dict[str, Any]) -> str:
    """MD5 hash of a dictionary."""
    dhash = hashlib.md5()
    # We need to sort arguments so {'a': 1, 'b': 2} is
    # the same as {'b': 2, 'a': 1}
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()

def lemmar_load(filename: str) -> tuple[int, list[str], bool, bool]:
    chosen_line: int = -1;
    status: list[str] = []
    done: bool = False
    won: bool = False
    data_to_check: dict[str, Any] = {}
    data_to_check[LEMMAR_DICT_IDX] = chosen_line
    data_to_check[LEMMAR_DICT_STS] = status
    data_to_check[LEMMAR_DICT_DONE] = done
    data_to_check[LEMMAR_DICT_WON] = won
    # Read from file and parse JSON
    full_filename = os.path.join(GAME_DATA_DIR, filename + ".json")
    if Path(full_filename).exists():
        # data = ""
        loaded_data = {}
        with open(full_filename, "r") as f:
            # data = json.load(f)
            loaded_data = json.load(f)
        # loaded_data = json.loads(data)
        chosen_line = loaded_data[LEMMAR_DICT_IDX]
        status = loaded_data[LEMMAR_DICT_STS]
        done = loaded_data[LEMMAR_DICT_DONE]
        won = loaded_data[LEMMAR_DICT_WON]
        # Setup a dictionary to check against
        data_to_check[LEMMAR_DICT_IDX] = chosen_line
        data_to_check[LEMMAR_DICT_STS] = status
        data_to_check[LEMMAR_DICT_DONE] = done
        data_to_check[LEMMAR_DICT_WON] = won
        # Compare the hash on file with the just calculated oe
        if dict_hash(data_to_check) != loaded_data["hash"]:
            print("Saved Data Corrupted - Resetting Game")
            chosen_line = -1
            status = []
            done = False
            won = False
    else:
        # print("No Saved Data exists")
        chosen_line = -1
        status = []
        done = False
        won = False
    return (chosen_line, status, done, won)

def lemmar_save(filename: str, chosen_line: int, status: list[str], done: bool, won: bool) -> None:
    data_to_save: dict[str, Any] = {}
    data_to_save[LEMMAR_DICT_IDX] = chosen_line
    data_to_save[LEMMAR_DICT_STS] = status
    data_to_save[LEMMAR_DICT_DONE] = done
    data_to_save[LEMMAR_DICT_WON] = won
    # Calculate a hash to detect data corruption
    hash = dict_hash(data_to_save)
    data_to_save["hash"] = hash
    # Create a JSON string and write it to file
    json_str = json.dumps(data_to_save, indent=4)
    full_filename = os.path.join(GAME_DATA_DIR, filename + ".json")
    with open(full_filename, "w") as f:
        f.write(json_str)

def get_word(filename: str, chosen_line: int) -> str:
    full_filename = os.path.join(WORD_DATA_DIR, filename)
    if Path(full_filename).exists():
        content = linecache.getline(full_filename, chosen_line)
        content = content.strip().upper()
        # print(f"Found: |{content}|")
    else:
        raise FileNotFoundError(f"{full_filename} not found")
    return content

def lemmar_new(filename: str) -> tuple[str, str, int] | None:
    try:
        line_count = bufcount(filename)
        if line_count > 0:
            content: str = ""
            count_blanks: int = 0
            chosen_line = -1
            while content == "" and count_blanks < 3:
                # Choose a new word
                chosen_line = randrange(1, line_count)
                content = get_word(filename, chosen_line)
                if re.fullmatch("^[A-Z]+", content) is None:
                    content = ""
                if content == "":
                    # Track blanks so we can limit failed reads to 3 in a row
                    count_blanks += 1
            if content == "":
                return (f"Failed: {count_blanks}, {filename}, {line_count}", "", -1)
            else:
                return (f"Found: {content}, {filename}, {chosen_line}/{line_count}"
                    , f"https://en.wiktionary.org/wiki/{content}"
                    , chosen_line)
    except FileNotFoundError as e:
        return (f"Error: FileNotFoundError, {e}", "", -2)
    return None

if __name__ == "__main__":
    # input = "0123456789"
    # index = 5
    # char = "V"
    # if len(sys.argv) > 1:
    #     input = sys.argv[1]
    # if len(sys.argv) > 2:
    #     index = int(sys.argv[2])
    # if len(sys.argv) > 3:
    #     char = sys.argv[3]
    # output = amend_string(input, index, char)
    # print(f"output: {output}")
    if len(sys.argv) > 1 and sys.argv[1] != "":
        print(lemmar_new(sys.argv[1]))
    else:
        print(lemmar_new("WORDS_5.txt"))
