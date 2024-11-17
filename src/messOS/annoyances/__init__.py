from pathlib import Path
from subprocess import Popen, DEVNULL
import random
import glob

MUSIC_DIR = Path(__file__).parent / "music"

def play_random_music():
    music_files = glob.glob(str(MUSIC_DIR / "*"))
    Popen(['vlc', random.choice(music_files)], stderr=DEVNULL, stdout=DEVNULL)