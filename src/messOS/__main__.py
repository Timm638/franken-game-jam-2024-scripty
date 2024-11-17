import random
import sys
import os
import subprocess
import platform
import shutil
from time import sleep
from typing import Literal

from messOS.tasks import Task
from messOS.tasks.sort_files import SortFilesTask
from messOS.tasks.shred_files import ShredTask
from messOS.filesystem import STATE_DIR

from termcolor import colored, cprint


def clear():
    for _ in range(300):
        print('\n')

def frame():
    sleep(cycle_time)
    clear()

def do_eternal_loading():
    loading_strings = [
        '/ -',
        '- -',
        '\\ -',
        '| -'
    ]
    loading_text = 'LOADING'
    loading_colors = ['white', 'yellow']
    max_i = 8
    while True:
        for i in range(0, max_i):
            print(colored(loading_strings[i%4], 'white'), colored(loading_text, loading_colors[int(i / 4)]))
            sleep(cycle_time)
            clear()


def draw_gibberish():
    gibberish_chars = '▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐▔▕🬀🬁🬂🬃🬄🬅🬆🬇🬈🬉🬊🬋🬌🬍🬎🬏🬐🬒🬑🬒🬓🬔🬕🬖🬗🬘🬙🬚🬛🬜🬝🬞🬟🬠🬡🬢🬣🬤🬥🬦🬦🬦🬧🬦🬧🬨🬩🬪🬫🬬🬭🬮🬯🬰🬱🬲🬳🬴🬵🬶🬷🬸🬹🬺🬻'
    for i in range(0, 64):
        cur_line = ''
        for j in range(0, 64):
            cur_line += random.choice(gibberish_chars)
        print(cur_line)

def draw_tasklist() -> None:
    print('-= TASKLIST =-')
    for task in tasks:
        is_finished: bool = task.is_completed()
        text_color: Literal['white', 'green'] = 'white' if not is_finished else 'green'
        finish_char ='✓' if is_finished else ' '
        print(colored('[' + finish_char + '] - ' + task.get_display_name(), color=text_color))

def all_tasks_fulfilled() -> bool:
    for task in tasks:
        if not task.is_completed():
            return False
    return True

def add_task():
    #component_list = [SortFilesTask]
    component_list = [ShredTask]
    tasks.append(random.choice(component_list)())

def main():
    # prepare game
    if os.path.exists(STATE_DIR):
        shutil.rmtree(STATE_DIR)
    os.mkdir(STATE_DIR)
    
    match platform.system():
        case "Windows": subprocess.Popen(f'explorer "{STATE_DIR}"')
        case "Linux": subprocess.Popen(['xdg-open', STATE_DIR])
        case "Darwin": subprocess.Popen(['open', STATE_DIR])

    add_task()

    while True:
        if all_tasks_fulfilled():
            add_task()
        draw_tasklist()
        frame()

### run module ###
cycle_time = 0.1

tasks: list[Task] = []


main()
