import copy
import os
import random
from pathlib import Path
import shutil

from . import Task, Scenario, TaskProgress
from messOS.filesystem import STATE_DIR

class ResearchScenario(Scenario):

    items : list
    folder_name : str

    def __init__(self, items, folder_name):
        self.items = items
        self.folder_name = folder_name

    def __deepcopy__(self, memodict={}):
        new_scenario = ResearchScenario(self.folders, self.items, self.folder_name)
        new_scenario.folders = copy.deepcopy(self.folders)
        new_scenario.items = copy.deepcopy(self.items)
        new_scenario.folder_name = copy.deepcopy(self.folder_name)
        return new_scenario

scenarios =  [
    ResearchScenario(
        [
            ('genesis_chapter_1_verse_28.txt', ['fruitful', 'earth', 'creature']),
            ('romans_chapter_12_verse_12.txt', ['joyful', 'affliction', 'prayer']),
            ('psalm_chapter_9_verse_9.txt', ['refuge', 'stronghold', 'prayer']),
        ],
        'to_research_in_english'
    ),
    ResearchScenario(
        [
            ('quran_chapter_66_verse_6.txt', ['families', 'angels', 'commanded']),
            ('romans_chapter_2_verse_45.txt', ['patience', 'prayer', 'submissive']),
            ('psalm_chapter_84_verse_25.txt', ['believe', 'righteous', 'uninterrupted']),
        ],
        'to_research_in_english'
    ),
    ResearchScenario(
        [
            ('MINECRAFT__blast_resistance_of_obsidian.txt', ['1200']),
            ('TERRARIA_use_time_of_drax.txt', ['15']),
            ('AMONG_US_max_player_count.txt', ['15']),
        ],
        'to_research_in_english'
    )
]


class ResearchFilesTask(Task):

    description : str
    task_folder : Path
    scenario : ResearchScenario

    def __init__(self, scenario = None):
        self.scenario = copy.deepcopy(random.choice(scenarios)) if not scenario else scenario
        self.description = 'Research the items in \'{0}\''.format(self.scenario.folder_name)
        self.reset()
    
    def get_display_name(self):
        return self.description

    def check_progress(self):
        pass
    
    def get_current_progress(self):
        return TaskProgress.IN_PROGRESS

    def is_completed(self) -> bool:
        # shortcut
        if os.path.isfile(self.task_folder / 'done'):
            return True
        # for every item
        for item in self.scenario.items:
            folder_name = self.scenario.folders[item[2]]
            if not os.path.isfile(self.task_folder / folder_name / item[0]):
                return False
        # TODO: Check if every file still exists, if not restore it in task_dir
        return True

    # Severity from 0 to 10 (reset)
    def fuck_u (self, severity: int):
        self.reset()


    def create_file(self, file_path: Path, file_content: str = 'No content given. :)'):
        f = open(self.task_folder / file_path, 'w')  # open file in append mode
        f.write(file_content)
        f.close()

    def reset(self):
        self.task_folder = STATE_DIR / Path(self.scenario.folder_name)
        if os.path.exists(self.task_folder):
            shutil.rmtree(self.task_folder)
        os.mkdir(self.task_folder)
        # Setup folders
        for folder in self.scenario.folders:
            os.mkdir(self.task_folder / Path(folder))
        # Setup items
        for item in self.scenario.items:
            self.create_file(item[0], item[1])
        pass