import os

## Project root directory
ROOT_DIR: str = os.path.abspath(os.curdir)
## Project data directory
DATA_DIR: str = os.path.join(ROOT_DIR, 'data')
## Word data directory
WORD_DATA_DIR: str = os.path.join(DATA_DIR, 'word')
## Game data directory
GAME_DATA_DIR: str = os.path.join(DATA_DIR, 'game')
### Project source directory
SRC_DIR: str = os.path.join(ROOT_DIR, 'src') ### Source folder
