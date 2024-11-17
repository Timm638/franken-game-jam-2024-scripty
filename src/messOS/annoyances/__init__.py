from pathlib import Path
import subprocess
import random
import glob

MUSIC_DIR = Path(__file__).parent / "music"

def play_random_music():
    music_files = glob.glob(str(MUSIC_DIR / "*"))
    subprocess.Popen(['vlc', random.choice(music_files)])