# shared_state.py

# This file defines constants for the global interaction state of the robot,
# allowing different processes to share a common understanding of the robot's status.

STATE_IDLE = 0        # Doing nothing, available for interaction
STATE_LISTENING = 1   # Actively listening for a user's command
STATE_SPEAKING = 2    # Playing back a TTS audio response
STATE_PROCESSING = 3  # Processing a command (e.g., waiting for LLM or KB response)
STATE_ERROR = -1      # An error has occurred in a major subsystem
