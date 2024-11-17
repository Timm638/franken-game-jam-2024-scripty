import math
import random
import sys
import os
import subprocess
import platform
import shutil
from time import sleep
from typing import Literal

from messOS.tasks import Task
from messOS.tasks.research_literature import ResearchFilesTask
from messOS.tasks.sort_files import SortFilesTask
from messOS.tasks.shred_files import ShredTask
from messOS.filesystem import STATE_DIR

from termcolor import colored, cprint


def clear():
    for _ in range(300):
        print('\n')

def frame(print_list: list[str], duration: float):
    for line in print_list:
        print(line)
    sleep(duration)
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


def print_gibberish():
    gibberish_chars = '▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐▔▕🬀🬁🬂🬃🬄🬅🬆🬇🬈🬉🬊🬋🬌🬍🬎🬏🬐🬒🬑🬒🬓🬔🬕🬖🬗🬘🬙🬚🬛🬜🬝🬞🬟🬠🬡🬢🬣🬤🬥🬦🬦🬦🬧🬦🬧🬨🬩🬪🬫🬬🬭🬮🬯🬰🬱🬲🬳🬴🬵🬶🬷🬸🬹🬺🬻'
    for i in range(0, 64):
        cur_line = ''
        for j in range(0, 64):
            cur_line += random.choice(gibberish_chars)
        print(cur_line)


def draw_gibberish_on(print_list: list[str], gibber_percentage: float = 0.5):
    gibberish_chars = '▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐▔▕🬀🬁🬂🬃🬄🬅🬆🬇🬈🬉🬊🬋🬌🬍🬎🬏🬐🬒🬑🬒🬓🬔🬕🬖🬗🬘🬙🬚🬛🬜🬝🬞🬟🬠🬡🬢🬣🬤🬥🬦🬦🬦🬧🬦🬧🬨🬩🬪🬫🬬🬭🬮🬯🬰🬱🬲🬳🬴🬵🬶🬷🬸🬹🬺🬻'
    output_list = []
    for line in print_list:
        output_line = ''
        for i in range(0, len(line)):
            output_line += line[i] if random.random() > gibber_percentage else random.choice(gibberish_chars)
        output_list.append(output_line)
    return output_list


def draw_tasklist() -> list[str]:
    output_list = ['-= TASKLIST =-']
    for task in tasks:
        is_finished: bool = task.is_completed()
        text_color: Literal['white', 'green'] = 'white' if not is_finished else 'green'
        finish_char ='✓' if is_finished else ' '
        output_list.append(colored('[' + finish_char + '] - ' + task.get_display_name(), color=text_color))
    return output_list

def all_tasks_fulfilled() -> bool:
    for task in tasks:
        if not task.is_completed():
            return False
    return True

def add_task():
    component_list = [ResearchFilesTask]
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

    cycle_time = 0.1


    gibber_duration = math.ceil(2.0 / cycle_time)
    gibber_percentage = 0.8
    cur_gibber_duration : int = 0

    while True:
        if all_tasks_fulfilled():
            add_task()
            cur_gibber_duration = gibber_duration
        l = draw_tasklist()
        if cur_gibber_duration > 0:
            l = draw_gibberish_on(l, gibber_percentage * (cur_gibber_duration/gibber_duration))
            cur_gibber_duration -= 1
        frame(l, cycle_time)

### run module ###


tasks: list[Task] = []


main()
