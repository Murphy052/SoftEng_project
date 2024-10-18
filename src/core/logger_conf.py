import logging

from src.core import settings


class ColorfulFormatter(logging.Formatter):
    COLOR_CODES = {
        'DEBUG': '\033[94m',  # Blue
        'INFO': '\033[92m',  # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',  # Red
        'CRITICAL': '\033[95m',  # Magenta
        'RESET': '\033[0m',  # Reset
        'WHITE': '\033[97m'  # White
    }

    LOG_FORMAT = (
        "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
    )

    def format(self, record):
        log_msg = super().format(record)
        message_start_index = log_msg.find(record.getMessage())
        prefix = log_msg[:message_start_index]
        message = log_msg[message_start_index:]

        color = self.COLOR_CODES.get(record.levelname, self.COLOR_CODES['RESET'])
        return f"{color}{prefix}{self.COLOR_CODES['WHITE']}{message}{self.COLOR_CODES['RESET']}"


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()

formatter = ColorfulFormatter(ColorfulFormatter.LOG_FORMAT)
handler.setFormatter(formatter)

logger.addHandler(handler)
if settings.DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
