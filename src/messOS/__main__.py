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
from messOS.tasks.backup_files import BackupTask
from messOS.tasks.research_literature import ResearchFilesTask, research_scenarios
from messOS.tasks.sort_files import SortFilesTask, SortScenario, sort_scenarios
from messOS.tasks.shred_files import ShredTask, shred_scenarios
from messOS.filesystem import STATE_DIR, PROJECT_DIR

from messOS.annoyances import REGISTERED_ANNOY

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
    component_list = [ShredTask, ResearchFilesTask, SortFilesTask, BackupTask]
    tasks.append(random.choice(component_list)())

def amount_completed_tasks() -> int:
    completed_tasks = list(filter(lambda task: task.is_completed(), tasks))
    return len(completed_tasks)

def draw_annoying_quotes(max_score : int):
    completed = amount_completed_tasks()
    quotes = [
        '',
        '',
        '',
        '',
        'Are ya winning son?',
        'Are ya winning son?',
        'Are ya winning son?',
        'Are ya winning son?',
        'Are ya winning son?',
        'Are ya winning son?',
    ]
    if max_score < len(quotes) and completed < len(quotes):
        return [quotes[completed]]
    else:
        return ['Max Score: {0}'.format(max_score)]

def sabotage_random_completed_task():
    for i in range(0, 10):
        chosen_task = random.choice(tasks)
        if chosen_task.is_completed():
            chosen_task.sabotage()
            subprocess.Popen(['cvlc', PROJECT_DIR / 'src' / 'messOS' / 'resources' / 'mlg_horn.mp3'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            return

def main():
    # prepare game
    if os.path.exists(STATE_DIR):
        shutil.rmtree(STATE_DIR)
    os.mkdir(STATE_DIR)
    
    match platform.system():
        case "Windows": subprocess.Popen(f'explorer "{STATE_DIR}"')
        case "Linux": subprocess.Popen(['xdg-open', STATE_DIR])
        case "Darwin": subprocess.Popen(['open', STATE_DIR])

    global tasks
    tasks = [
        BackupTask(),
    SortFilesTask(scenario=sort_scenarios[0]),
SortFilesTask(scenario=sort_scenarios[1]),
SortFilesTask(scenario=sort_scenarios[2]),
ResearchFilesTask(scenario=research_scenarios[0]),
ResearchFilesTask(scenario=research_scenarios[1]),
ResearchFilesTask(scenario=research_scenarios[2]),
    ShredTask(scenario=shred_scenarios[0]),
ShredTask(scenario=shred_scenarios[1]),
ShredTask(scenario=shred_scenarios[2])
        ]

    cycle_time = 0.1

    gibber_duration = math.ceil(2.0 / cycle_time)
    gibber_percentage = 0.8
    cur_gibber_duration : int = 0

    max_score = 0

    frame_count = 0

    annoyance_probabilities = [
        0,    0,   0,    0.003, 0.005,
        0.015, 0.02, 0.03, 0.04,  0.05 ]

    while True:
        max_score = max(max_score, amount_completed_tasks())
        # max index of 10
        annoyance_index = min(amount_completed_tasks(), len(annoyance_probabilities) - 1)

        if annoyance_probabilities[annoyance_index] >= random.random():
            if random.random() > 0.7:
                random.choice(REGISTERED_ANNOY)()
            else:
                sabotage_random_completed_task()

        if all_tasks_fulfilled():
            add_task()
            cur_gibber_duration = gibber_duration

        l_aq = draw_annoying_quotes(max_score)
        l = draw_tasklist()
        l = l_aq + l
        if cur_gibber_duration > 0:
            l = draw_gibberish_on(l, gibber_percentage * (cur_gibber_duration/gibber_duration))
            cur_gibber_duration -= 1
        frame(l, cycle_time)
        frame_count += 1

### run module ###

tasks: list[Task] = []


main()
