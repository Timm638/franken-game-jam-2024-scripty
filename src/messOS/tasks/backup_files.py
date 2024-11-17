import copy
import os
import random
import uuid
from pathlib import Path
import shutil

from . import Task, Scenario, TaskProgress
from messOS.filesystem import STATE_DIR

class BackupTask(Task):

    description : str
    task_folder : Path
    uuid : str

    def __init__(self, scenario = None):
        self.task_folder = STATE_DIR / Path('I_WILL_DELETE_MYSELF')
        if os.path.isdir(self.task_folder):
            # Fallback option
            self.task_folder = STATE_DIR / Path(str(next(Task.id_iter))+ '_I_WILL_DELETE_MYSELF')
        self.description = '[URGENT] Backup the folder \'{0}\''.format(self.task_folder.name)
        self.uuid = str(uuid.uuid4())
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
        if os.path.isfile(self.task_folder / 'the_best_joke_ever'):
            with open(self.task_folder / 'the_best_joke_ever', 'r') as f:
                if self.uuid in f.read():
                    return True
        return False

    def sabotage (self):
        os.remove(self.task_folder / 'the_best_joke_ever')


    def create_file(self, file_path: Path, file_content: str = 'No content given. :)'):
        f = open(self.task_folder / file_path, 'w')  # open file in append mode
        f.write(file_content)
        f.close()

    def reset(self):
        if os.path.exists(self.task_folder):
            shutil.rmtree(self.task_folder)
        os.mkdir(self.task_folder)
        self.create_file('the_best_joke_ever', self.uuid)
        pass