import copy
import os
import random
from pathlib import Path
import shutil

class _Scenario:

    folders : list
    items : list

    def __init__(self, folders, items):
        self.folders = folders
        self.items = items

    def __deepcopy__(self, memodict={}):
        new_scenario = _Scenario(self.folders, self.items)
        new_scenario.folders = copy.deepcopy(self.folders)
        new_scenario.items = copy.deepcopy(self.items)
        return new_scenario

scenarios =  [
    _Scenario(
        [
            '1_documents',
            '2_music',
            '3_tax_documents'
        ],
        [
            ('work_report.txt', 'FEBRUARY 2025', 0),
            ('your_perfect_partner_theme_doodle.mp3', 'Dododoo do dod do dooooo do', 1),
            ('tax_evasion.pdf', ':)', 2),
        ]
    ),
_Scenario(
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
        ]
    ),
_Scenario(
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
        ]
    ),
_Scenario(
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
        ]
    )
]

class SortFilesTask:

    description : str
    task_folder : Path
    scenario : _Scenario

    def __init__(self):
        self.description = 'Sort your files'
        self.scenario = copy.deepcopy(scenarios[3])
        self.reset()

    def check(self) -> bool:
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


    def create_file(self, file_path : Path, file_content : str = 'No content given. :)'):
        f = open(self.task_folder / file_path, 'w')  # open file in append mode
        f.write(file_content)
        f.close()

    def reset(self):
        self.task_folder = Path(os.getcwd()) / Path('to_sort')
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