import pyaudio
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ListAudioDevices")

if __name__ == "__main__":
    p = None
    try:
        logger.info("Initializing PyAudio...")
        p = pyaudio.PyAudio()
        
        info = p.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')

        logger.info(f"--- Available Audio Devices ({num_devices} total) ---")
        for i in range(0, num_devices):
            device_info = p.get_device_info_by_host_api_device_index(0, i)
            logger.info(f"  Device Index: {i}")
            logger.info(f"    Name: {device_info.get('name')}")
            logger.info(f"    Input Channels: {device_info.get('maxInputChannels')}")
            logger.info(f"    Output Channels: {device_info.get('maxOutputChannels')}")
            logger.info(f"    Sample Rate: {device_info.get('defaultSampleRate')}")
            logger.info("-" * 40)
        logger.info("------------------------------------")
        logger.info("Identify your desired output device (speakers) and note its 'Device Index'.")

    except Exception as e:
        logger.error(f"Error listing audio devices: {e}", exc_info=True)
        logger.error("Ensure PyAudio is correctly installed and your audio system is functional.")
    finally:
        if p:
            logger.info("Terminating PyAudio.")
            p.terminate()
