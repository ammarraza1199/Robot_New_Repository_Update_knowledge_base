import logging
import sys
from logging.handlers import TimedRotatingFileHandler

# ==============================================================================
# Centralized Logging Configuration
# ==============================================================================

# Configuration
LOG_FILE_NAME = "logs/robot_run.log"
LOG_FORMAT = '%(asctime)s - %(processName)s - %(name)s - %(levelname)s - %(message)s'

def setup_logging():
    """
    Configures a rotating file logger for all processes.
    This should be called once at the beginning of each process.
    """
    # Get the root logger
    root_logger = logging.getLogger()
    
    # Avoid adding handlers multiple times in the same process
    if root_logger.hasHandlers():
        # If handlers are already configured, assume it's set up
        return

    root_logger.setLevel(logging.DEBUG)  # Capture all levels of logs

    # Create a handler that rotates the log file daily
    # It will keep the last 7 log files.
    file_handler = TimedRotatingFileHandler(
        LOG_FILE_NAME, 
        when="midnight",          # Rotate at midnight
        interval=1,               # Daily rotation
        backupCount=7,            # Keep 7 old log files
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG) # Log everything to the file
    
    # Create a formatter and set it for the handler
    formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(formatter)
    
    # Add the handler to the root logger
    root_logger.addHandler(file_handler)

    # Also, add a handler to print INFO level logs to the console for real-time feedback
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG) # Only show INFO and above on console
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    logger = logging.getLogger(__name__)
    logger.info("="*50)
    logger.info("Logging configured: outputting to console (INFO) and daily rotating file (DEBUG).")
    logger.info("="*50)

