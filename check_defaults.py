import pyaudio
import speech_recognition as sr
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_default_devices():
    p = pyaudio.PyAudio()

    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')

    default_input_index = None
    default_output_index = None

    try:
        default_input_device = p.get_default_input_device_info()
        default_input_index = default_input_device['index']
        logging.info(f"System Default Input Device (Microphone):")
        logging.info(f"  Name: {default_input_device['name']}")
        logging.info(f"  Index: {default_input_device['index']}")
        logging.info(f"  Host API: {p.get_host_api_info_by_index(default_input_device['hostApi'])['name']}")
        logging.info(f"  Max Input Channels: {default_input_device['maxInputChannels']}")
    except OSError:
        logging.warning("No default input device found or accessible.")

    try:
        default_output_device = p.get_default_output_device_info()
        default_output_index = default_output_device['index']
        logging.info(f"\nSystem Default Output Device (Speaker):")
        logging.info(f"  Name: {default_output_device['name']}")
        logging.info(f"  Index: {default_output_device['index']}")
        logging.info(f"  Host API: {p.get_host_api_info_by_index(default_output_device['hostApi'])['name']}")
        logging.info(f"  Max Output Channels: {default_output_device['maxOutputChannels']}")
    except OSError:
        logging.warning("No default output device found or accessible.")

    logging.info("\n--- All Audio Devices ---")
    for i in range(0, num_devices):
        if p.get_device_info_by_host_api_device_index(0, i)['maxInputChannels'] > 0 or \
           p.get_device_info_by_host_api_device_index(0, i)['maxOutputChannels'] > 0:
            
            dev_info = p.get_device_info_by_host_api_device_index(0, i)
            is_default_input = " (DEFAULT MICROPHONE)" if i == default_input_index else ""
            is_default_output = " (DEFAULT SPEAKER)" if i == default_output_index else ""

            logging.info(f"\nDevice Index: {i}{is_default_input}{is_default_output}")
            logging.info(f"  Name: {dev_info['name']}")
            logging.info(f"  Host API: {p.get_host_api_info_by_index(dev_info['hostApi'])['name']}")
            logging.info(f"  Input Channels: {dev_info['maxInputChannels']}")
            logging.info(f"  Output Channels: {dev_info['maxOutputChannels']}")

    p.terminate()

if __name__ == "__main__":
    get_default_devices()
