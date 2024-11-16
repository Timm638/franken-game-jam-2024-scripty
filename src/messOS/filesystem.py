from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent.parent
STATE_DIR = PROJECT_DIR / "MESS_WITH_ME"