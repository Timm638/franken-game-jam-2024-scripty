from abc import ABC, abstractmethod
from typing import Union
from enum import Enum, auto

class TaskProgress(Enum):
    UNTOUCHED = auto()
    IN_PROGRESS = auto()
    FINISHED = auto()

class Scenario(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

class Task(ABC):
    @abstractmethod
    def __init__(self, scenario: Union[Scenario, None]):
        pass

    @abstractmethod
    def get_current_progress(self) -> TaskProgress:
        pass

    def is_completed(self) -> bool:
        return self.get_current_progress() == TaskProgress.FINISHED
    
    @abstractmethod
    def get_display_name(self) -> str:
        pass
    