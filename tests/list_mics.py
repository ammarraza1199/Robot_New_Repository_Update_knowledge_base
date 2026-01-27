import speech_recognition as sr
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ListMics")

if __name__ == "__main__":
    logger.info("Attempting to list all available microphones and their indices...")
    try:
        # Use list_microphone_names() and enumerate to get names and indices
        microphone_names = sr.Microphone.list_microphone_names()
        
        if not microphone_names:
            logger.warning("No microphones found by SpeechRecognition.")
        else:
            logger.info("--- Available Microphones ---")
            for index, name in enumerate(microphone_names):
                logger.info(f"Name: {name}, Index: {index}")
            logger.info("-----------------------------")
            logger.info("Please identify the index for your desired microphone (e.g., miniDSP).")
    except Exception as e:
        logger.error(f"Error listing microphones: {e}", exc_info=True)
        logger.error("Ensure PyAudio is correctly installed and your audio devices are recognized by the system.")