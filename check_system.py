import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def run_health_check():
    """
    Performs basic system health checks to ensure the robot can start.
    Returns True if all checks pass, False otherwise.
    """
    logger.info("Running system health checks...")

    # Check for essential environment variables
    load_dotenv()
    if not os.environ.get("GROQ_API_KEY"):
        logger.error("Health Check Failed: GROQ_API_KEY environment variable not set.")
        return False

    # Check for existence of critical script files
    essential_scripts = [
        "vision_process.py",
        "interaction_process.py",
        "pyaudio_player.py",
        "motor_control_process.py",
        "logging_config.py",
    ]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    all_scripts_present = True
    for script in essential_scripts:
        script_path = os.path.join(script_dir, script)
        if not os.path.exists(script_path):
            logger.error(f"Health Check Failed: Essential script '{script}' not found at '{script_path}'.")
            all_scripts_present = False
            
    if not all_scripts_present:
        return False

    logger.info("All system health checks passed.")
    return True
