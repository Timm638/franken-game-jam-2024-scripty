import random
import sys
import os
from time import sleep

from messOS.tasks.sortFiles import SortFilesTask

from termcolor import colored, cprint

cycle_time = 0.1

tasks = []
tasks.append(SortFilesTask())

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

def draw_tasklist():
    for task in tasks:
        is_finished : bool = task.check()
        text_color = 'white' if not is_finished else 'green'
        finish_char ='✓' if is_finished else ' '
        print(colored('[' + finish_char + '] - ' + task.description, color=text_color))

while True:
    draw_gibberish()
    frame()



