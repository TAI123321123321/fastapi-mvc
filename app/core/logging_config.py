"""
Logging configuration for the application.
This module should be imported first to configure logging before uvicorn starts.
"""
import logging
import sys
import os

# ANSI color codes for terminal colors
class Colors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Text colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log levels"""
    
    # Color mapping for log levels
    LEVEL_COLORS = {
        'DEBUG': Colors.CYAN,
        'INFO': Colors.GREEN,
        'WARNING': Colors.YELLOW,
        'ERROR': Colors.RED,
        'CRITICAL': Colors.BRIGHT_RED,
    }
    
    def format(self, record):
        # Get the color for this log level
        level_color = self.LEVEL_COLORS.get(record.levelname, Colors.WHITE)
        
        # Colorize the level name
        record.levelname = f"{level_color}{record.levelname}{Colors.RESET}"
        
        # Format the message
        return super().format(record)


# Configure logging as early as possible, even before uvicorn imports
# This ensures all logs including uvicorn startup logs have timestamps
_log_format = '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
_date_format = '%Y-%m-%d %H:%M:%S'

# Configure root logger first with colored formatter
root_logger = logging.getLogger()
root_logger.handlers = []
root_handler = logging.StreamHandler(sys.stdout)
root_handler.setFormatter(ColoredFormatter(_log_format, datefmt=_date_format))
root_logger.addHandler(root_handler)
root_logger.setLevel(logging.INFO)

# Configure basic logging with colored formatter
logging.basicConfig(
    level=logging.INFO,
    format=_log_format,
    datefmt=_date_format,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ],
    force=True  # Override any existing configuration
)

# Replace default formatter with colored formatter for root logger
for handler in logging.root.handlers:
    if isinstance(handler, logging.StreamHandler):
        handler.setFormatter(ColoredFormatter(_log_format, datefmt=_date_format))


def setup_logging():
    """Configure logging with timestamp format and colors for all loggers including uvicorn"""
    colored_formatter = ColoredFormatter(_log_format, datefmt=_date_format)
    
    # Configure uvicorn loggers to use the same format with colors
    # This must be done early to catch uvicorn startup logs
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers = []
    uvicorn_handler = logging.StreamHandler(sys.stdout)
    uvicorn_handler.setFormatter(colored_formatter)
    uvicorn_logger.addHandler(uvicorn_handler)
    uvicorn_logger.setLevel(logging.INFO)
    uvicorn_logger.propagate = False

    # Configure uvicorn.access logger (for HTTP requests)
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = []
    uvicorn_access_handler = logging.StreamHandler(sys.stdout)
    uvicorn_access_handler.setFormatter(colored_formatter)
    uvicorn_access_logger.addHandler(uvicorn_access_handler)
    uvicorn_access_logger.setLevel(logging.INFO)
    uvicorn_access_logger.propagate = False

    # Configure uvicorn.error logger
    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_error_logger.handlers = []
    uvicorn_error_handler = logging.StreamHandler(sys.stdout)
    uvicorn_error_handler.setFormatter(colored_formatter)
    uvicorn_error_logger.addHandler(uvicorn_error_handler)
    uvicorn_error_logger.setLevel(logging.INFO)
    uvicorn_error_logger.propagate = False


# Setup logging immediately when this module is imported
setup_logging()

# Also configure uvicorn loggers immediately (in case they're already created)
colored_formatter = ColoredFormatter(_log_format, datefmt=_date_format)
for logger_name in ["uvicorn", "uvicorn.access", "uvicorn.error"]:
    logger = logging.getLogger(logger_name)
    if logger.handlers:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(colored_formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False

