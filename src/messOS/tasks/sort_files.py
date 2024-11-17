import copy
import os
import random
from pathlib import Path
import shutil

from . import Task, Scenario, TaskProgress
from messOS.filesystem import STATE_DIR

class SortScenario(Scenario):

    folders : list
    items : list
    folder_name : str

    def __init__(self, folders, items, folder_name):
        self.folders = folders
        self.items = items
        self.folder_name = folder_name

    def __deepcopy__(self, memodict={}):
        new_scenario = SortScenario(self.folders, self.items, self.folder_name)
        new_scenario.folders = copy.deepcopy(self.folders)
        new_scenario.items = copy.deepcopy(self.items)
        new_scenario.folder_name = copy.deepcopy(self.folder_name)
        return new_scenario
    
    def get_name(self) -> str:
        return self.folder_name

scenarios =  [
    SortScenario(
        [
            '1_documents',
            '2_music',
            '3_tax_documents'
        ],
        [
            ('work_report.txt', 'FEBRUARY 2025', 0),
            ('your_perfect_partner_theme_doodle.mp3', 'Dododoo do dod do dooooo do', 1),
            ('tax_evasion.pdf', ':)', 2),
        ],
        'home'
    ),
    SortScenario(
        [
            '1_democratic',
            '2_republican',
        ],
        [
            ('barack____obama.char', '', 0),
            ('donald____trump.char', '', 1),
            ('joe_______biden.char', '', 0),
            ('george_w__bush.char', '', 1),
            ('bill______clinton.char', '', 0),
            ('george_hw_bush.char', '', 1),
            ('ronald____reagan.char', '', 1),
            ('jimmy_____carter.char', '', 0),
            ('gerald____ford.char', '', 1),
            ('richard___nixon.char', '', 1),
            ('john____f_kennedy.char', '', 0),
        ],
    'free_country'
    ),
    SortScenario(
        [
            '0_Who_has_Paul_thanked_for_each_location_in_keynote',
            '1_Bamberg',
            '2_Coburg',
            '3_Bayreuth',
            '4_Nuremberg',
            '5_Wuerzburg',
            '6_Hof',
        ],
        [
            ('luise.char', '', 1),
            ('alisa.char', '', 2),
            ('laura.char', '', 3),
            ('sebastian.char', '', 4),
            ('linda.char', '', 5),
            ('andy.char', '', 6),
        ],
        'franken_game_jam_2024'
    ),
    SortScenario(
        [
            'Actions',
            'Strategy',
            'RPG',
            'Sandbox'
        ],
        [
            ('battlef1eld', '', 0),
            ('call_of_duti', '', 0),
            ('civilization', '', 1),
            ('minceraft', '', 3),
            ('final_fantasi', '', 2),
        ],
        'games'
    )
]

class SortFilesTask(Task):

    description : str
    task_folder : Path
    scenario : SortScenario

    def __init__(self, scenario = None):
        self.scenario = copy.deepcopy(random.choice(scenarios)) if not scenario else scenario
        self.description = 'Sort the folder \'{0}\''.format(self.scenario.folder_name)
        self.reset()
    
    def get_display_name(self):
        return self.description

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