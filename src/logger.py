import logging
import os
import sys

from config import CONFIG

DEBUG = CONFIG.DEBUG

class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[1;36m",   # Cyan
        "INFO": "\033[1;32m",    # Green
        "WARNING": "\033[1;33m", # Yellow
        "ERROR": "\033[1;31m",   # Red
        "CRITICAL": "\033[1;41m" # Red background
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        record.levelname = f"{color}[{record.levelname}]{self.RESET}"
        return super().format(record)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(ColorFormatter("[{asctime}] {levelname} {message}", style="{", datefmt="%H:%M:%S"))

log = logging.getLogger("crimbo")
log.setLevel(logging.DEBUG if DEBUG else logging.INFO)
log.handlers.clear()
log.addHandler(handler)
log.propagate = False
