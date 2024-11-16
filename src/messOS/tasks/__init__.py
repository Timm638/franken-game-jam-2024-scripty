from abc import ABC, abstractmethod

class Task(ABC):
    @abstractmethod
    def __init__(self, scenario: Scenario):
        pass

    @abstractmethod
    def check_progress(self):
        pass
    
    @abstractmethod
    def is_completed(self) -> bool:
        pass
    
    @abstractmethod
    def get_display_name(self) -> str:
        pass
    
class Scenario(ABC):

    @abstractmethod
    def get_name(self) -> str:
        pass