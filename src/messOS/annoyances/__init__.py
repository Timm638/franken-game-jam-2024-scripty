import os
import shutil
from pathlib import Path
from subprocess import Popen, DEVNULL
import random
import glob
import uuid

from messOS.filesystem import STATE_DIR

MUSIC_DIR = Path(__file__).parent / "music"

def play_random_music():
    music_files = glob.glob(str(MUSIC_DIR / "*"))
    Popen(['vlc', random.choice(music_files)], stderr=DEVNULL, stdout=DEVNULL)

def produce_rabbit():
    rabbit_name = random.choice(['rabbit', 'ribbit', 'bunnny', 'garnickl', 'kaninchen'])
    rabbit_image_path = os.path.dirname(os.path.realpath(__file__)) / Path('../resources/rabbit.png')
    des_folder = random.choice(os.listdir(STATE_DIR))
    rabbit_des = STATE_DIR / des_folder / Path(rabbit_name + '_' + str(uuid.uuid4()) + '.png')
    shutil.copyfile(rabbit_image_path, rabbit_des)


