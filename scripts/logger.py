import logging

RESET = '\033[0m'
BOLD = '\033[1m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_CYAN = '\033[96m'

SUCCESS = 25
logging.addLevelName(SUCCESS, "SUCCESS")

class Logger(logging.Logger):
    def success(self, message: str, *args: object, **kwargs: object) -> None:
        if self.isEnabledFor(SUCCESS):
            self._log(SUCCESS, message, args, **kwargs)

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.INFO: BRIGHT_CYAN,
        SUCCESS: BRIGHT_GREEN,
        logging.ERROR: BRIGHT_RED,
    }

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, RESET)
        level = f"{color}{record.levelname:<2}{RESET}"
        message = f"{color}{BOLD}{record.getMessage()}{RESET}"
        return f"{level} {message}"

logging.setLoggerClass(Logger)

def get_logger(level: int = logging.INFO) -> Logger:
    logger = logging.getLogger("logger")
    logger.setLevel(level)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(ColorFormatter())
        logger.addHandler(handler)

    return logger