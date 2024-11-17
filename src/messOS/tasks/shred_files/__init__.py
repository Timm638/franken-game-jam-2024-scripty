import os
import random
import copy
import shutil
import glob
from pathlib import Path

from messOS.filesystem import STATE_DIR
from .. import Task, Scenario, TaskProgress

MODULE_DIR = Path(__file__).parent

class ShredScenario(Scenario):
    scenario_name: str

    folder_name: str
    desired_files: list[str]
    
    def __init__(self, scenario_name, folder_name, desired_files):
        self.scenario_name = scenario_name
        self.folder_name = folder_name
        self.desired_files = desired_files
    
    def get_name(self) -> str:
        return self.scenario_name
    
    def get_initial_files(self) -> list[str]:
        source_folder = MODULE_DIR / self.folder_name
        file_paths = glob.glob(str(source_folder / "*"))
        return list(map(os.path.basename, file_paths))


    
shred_scenarios = [
    ShredScenario(
        scenario_name="delete illegal documents",
        folder_name="Finances",
        desired_files=[
            'laundry_bill.doc',
            'internet_provider_invoice.doc',
            'beeg_yoshi.png'
        ]
    ),
    ShredScenario(
        scenario_name="cleanup the Homeworks folder",
        folder_name="Homeworks",
        desired_files=[
            'Latin.txt',
            'Math.txt',
            'philosophy.mkv'
        ]
    ),
]

class ShredTask(Task):
    scenario: ShredScenario
    progress: TaskProgress
    
    def __init__(self, scenario=random.choice(shred_scenarios)):
        self.scenario=scenario
        shred_scenarios.remove(self.scenario)
        
        folder_name = scenario.folder_name
        target_path = STATE_DIR / folder_name
        if os.path.exists(self.get_state_folder()):
            shutil.rmtree(self.get_state_folder())
        shutil.copytree(MODULE_DIR / folder_name, self.get_state_folder())

    def get_state_folder(self) -> Path:
        return STATE_DIR / self.scenario.folder_name
    
    def get_display_name(self) -> str:
        return self.scenario.get_name()
    
    def get_current_state(self) -> list[str]:
        state_folder = self.get_state_folder()
        current_state_filepaths = glob.glob(str(state_folder / '*'))
        return list(map(os.path.basename, current_state_filepaths))
    
    def get_current_progress(self) -> TaskProgress:
        desired_state = set(self.scenario.desired_files)
        initial_state = set(self.scenario.get_initial_files())
        current_state = set(self.get_current_state())

        if current_state == desired_state:
            return TaskProgress.FINISHED
        if initial_state == current_state:
            return TaskProgress.UNTOUCHED
        return TaskProgress.IN_PROGRESS