
import multiprocessing
import time
import os
import logging
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'tests'))

# Import the target functions from the new process modules
from vision_process import vision_process_func
from interaction_process import interaction_process_func
from pyaudio_player import pyaudio_player_process
from motor_control_process import motor_control_process
from logging_config import setup_logging
from check_system import run_health_check

# Set up logging for the main process
setup_logging()
logger = logging.getLogger("main")

if __name__ == "__main__":
    # --- System Health Check ---
    if not run_health_check():
        logger.critical("Startup Aborted: System Health Check Failed.")
        sys.exit(1)
        
    # Note: It's good practice for child processes to re-initialize logging
    # within their own target function to avoid multiprocessing issues.
    # The setup_logging() function is designed to be called in each process.
    
    logger.info("Starting main orchestrator...")

    # Create shared queues for inter-process communication
    audio_queue = multiprocessing.Queue()
    motor_queue = multiprocessing.Queue()
    audio_feedback_queue = multiprocessing.Queue()
    
    # Create a shutdown event that can be passed to processes
    shutdown_flag = multiprocessing.Event()

    # Create a flag to signal when audio is playing, to prevent feedback loops
    audio_playing_flag = multiprocessing.Event()

    # A dictionary to hold the processes
    processes = {
                "vision": multiprocessing.Process(
                    target=vision_process_func,
                    args=(audio_queue, shutdown_flag, audio_playing_flag, 'data/yolov8n.pt')
                ),        "interaction": multiprocessing.Process(
            target=interaction_process_func, 
            args=(audio_queue, motor_queue, shutdown_flag, audio_playing_flag, audio_feedback_queue)
        ),
        "audio": multiprocessing.Process(
            target=pyaudio_player_process, 
            args=(audio_queue, audio_feedback_queue, shutdown_flag)
        ),
        "motor": multiprocessing.Process(
            target=motor_control_process, 
            args=(motor_queue, shutdown_flag)
        )
    }

    # Start all processes
    for name, p in processes.items():
        logger.info(f"Starting {name} process...")
        p.start()

    # The main process will now act as a supervisor
    exit_code = 0  # Assume clean exit unless an essential process fails
    try:
        essential_processes = ["interaction", "audio"]
        
        while True:
            time.sleep(5) # Check process health every 5 seconds
            
            # Check for dead essential processes
            for name in essential_processes:
                if not processes[name].is_alive():
                    logger.critical(f"Essential process '{name}' has terminated unexpectedly. Initiating system shutdown.")
                    shutdown_flag.set()
                    exit_code = 1  # Set exit code to indicate failure
                    break # Exit the for loop
            
            if shutdown_flag.is_set():
                break # Exit the while loop to proceed with shutdown

            # Optional: Check and log non-essential process termination
            for name, p in processes.items():
                if name not in essential_processes and not p.is_alive():
                    # This process has died. We can log it, remove it from the dict to avoid re-checking,
                    # or even try to restart it. For now, we'll just log it.
                    logger.warning(f"Non-essential process '{name}' has terminated.")
                    # To prevent re-logging, we can remove it, but this requires a copy
                    # of the dictionary keys to iterate over, e.g., for name in list(processes.keys()):
    
    except KeyboardInterrupt:
        logger.info("\nMain: Shutdown signal received from KeyboardInterrupt. Terminating processes gracefully.")
        shutdown_flag.set()

        # Signal the queue-based processes to shut down
        audio_queue.put("shutdown")
        motor_queue.put("shutdown")

    # Wait for all processes to terminate
    logger.info("Main: Waiting for all processes to shut down.")
    for name, p in processes.items():
        p.join(timeout=10) # Add a timeout for joining
        if p.is_alive():
            logger.warning(f"Main: Process {name} did not terminate gracefully. Forcing termination.")
            p.terminate() # Force terminate if it's stuck

    logger.info("Main: All processes have been shut down.")
    sys.exit(exit_code)
