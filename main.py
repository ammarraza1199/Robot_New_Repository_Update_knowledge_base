
import multiprocessing
import time
import os
import logging

# Import the target functions from the new process modules
from vision_process import vision_process_func
from interaction_process import interaction_process_func
from pyaudio_player import pyaudio_player_process
from motor_control_process import motor_control_process
from logging_config import setup_logging
from check_system import run_health_check
import sys
<<<<<<< HEAD
=======
from shared_state import STATE_IDLE
>>>>>>> db2b1d0 (Initial commit)

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
<<<<<<< HEAD
    
    # Create a shutdown event that can be passed to processes
    shutdown_flag = multiprocessing.Event()

    # Create a flag to signal when audio is playing, to prevent feedback loops
    audio_playing_flag = multiprocessing.Event()
=======
    audio_feedback_queue = multiprocessing.Queue() # For audio player -> interaction process

    # Create a shutdown event that can be passed to processes
    shutdown_flag = multiprocessing.Event()

    # --- Create a shared value for global interaction state ---
    shared_interaction_state = multiprocessing.Value('i', STATE_IDLE)
>>>>>>> db2b1d0 (Initial commit)

    # A dictionary to hold the processes
    processes = {
        "vision": multiprocessing.Process(
            target=vision_process_func, 
<<<<<<< HEAD
            args=(audio_queue, shutdown_flag, audio_playing_flag)
        ),
        "interaction": multiprocessing.Process(
            target=interaction_process_func, 
            args=(audio_queue, motor_queue, shutdown_flag, audio_playing_flag)
        ),
        "audio": multiprocessing.Process(
            target=pyaudio_player_process, 
            args=(audio_queue, audio_playing_flag, shutdown_flag)
=======
            args=(audio_queue, shutdown_flag, shared_interaction_state)
        ),
        "interaction": multiprocessing.Process(
            target=interaction_process_func, 
            args=(audio_queue, motor_queue, audio_feedback_queue, shutdown_flag, shared_interaction_state)
        ),
        "audio": multiprocessing.Process(
            target=pyaudio_player_process, 
            args=(audio_queue, audio_feedback_queue, shutdown_flag)
>>>>>>> db2b1d0 (Initial commit)
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

    # The main process will wait for a KeyboardInterrupt (Ctrl+C) to shutdown.
    try:
        # Keep the main process alive. The child processes are daemonic
        # and will be terminated if the main process exits, but we want
        # to perform a graceful shutdown.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("\nMain: Shutdown signal received. Terminating processes gracefully.")
        
        # Set the shutdown flag for processes that use it
        shutdown_flag.set()

        # Signal the queue-based processes to shut down
        # It's good practice to send shutdown signals to all queue-based workers
        audio_queue.put("shutdown")
        motor_queue.put("shutdown")

    # Wait for all processes to terminate
    for name, p in processes.items():
        p.join(timeout=10) # Add a timeout for joining
        if p.is_alive():
            logger.warning(f"Main: Process {name} did not terminate gracefully. Forcing termination.")
            p.terminate() # Force terminate if it's stuck

    logger.info("Main: All processes have been shut down.")
