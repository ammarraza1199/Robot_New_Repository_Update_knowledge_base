import multiprocessing
import time
import logging
import serial
from logging_config import setup_logging

logger = logging.getLogger(__name__)

class MotorController:
    """
    Controls the neck motor by sending single characters ('L', 'R', 'C')
    over a serial connection based on commands from a queue.
    """
    def __init__(self, motor_queue, port='/dev/ttyS0', baud_rate=9600):
        self.motor_queue = motor_queue
        self.shutdown_flag = multiprocessing.Event()
        self.port = port
        self.baud_rate = baud_rate
        self.serial_connection = None
        self.serial_ok = False  # Track serial port state

        logger.info(f"Initializing motor controller for serial port {self.port} at {self.baud_rate} baud.")
        try:
            self.serial_connection = serial.Serial(self.port, self.baud_rate, timeout=1)
            logger.info("Successfully opened serial port.")
            self.serial_ok = True
        except serial.SerialException as e:
            logger.error(f"FATAL: Could not open serial port. Motor control will be disabled. Error: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred during serial initialization: {e}", exc_info=True)

    def cleanup(self):
        """Closes the serial connection if it is open."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            logger.info("Serial port closed.")

    def handle_command(self, message):
        """Parses motor commands, translates them to characters, and sends them."""
        logger.debug(f"Handling motor command: '{message}'")

        # --- Start of new health check logic ---
        if not self.serial_connection or not self.serial_connection.is_open:
            if self.serial_ok:  # It was previously ok, so this is the first failure
                logger.error("Motor command ignored: serial port is not open. Further motor logs will be suppressed.")
                self.serial_ok = False
            return  # Silently ignore the command

        if not self.serial_ok:  # It has just become available again
            logger.info("Serial port is now available. Motor commands will be processed.")
            self.serial_ok = True
        # --- End of new health check logic ---

        try:
            parts = message.split(':')
            command = parts[0]
            
            if command == 'turn_to':
                target_angle = int(parts[1])
                char_to_send = ''
                
                if target_angle > 5:  # Adding a small dead zone around 0
                    char_to_send = 'R' # Right
                    logger.info(f"Received angle {target_angle}°, sending 'R' for Right.")
                elif target_angle < -5:
                    char_to_send = 'L' # Left
                    logger.info(f"Received angle {target_angle}°, sending 'L' for Left.")
                else: # target_angle is between -5 and 5
                    char_to_send = 'C' # Center
                    logger.info(f"Received angle {target_angle}°, sending 'C' for Center.")
                
                logger.debug(f"Writing '{char_to_send}' to serial port.")
                self.serial_connection.write(char_to_send.encode('ascii'))
            
            elif command == 'turn_by':
                relative_angle = int(parts[1])
                char_to_send = ''

                if relative_angle > 5:
                    char_to_send = 'R'
                    logger.info(f"Received relative angle {relative_angle}°, sending 'R'.")
                elif relative_angle < -5:
                    char_to_send = 'L'
                    logger.info(f"Received relative angle {relative_angle}°, sending 'L'.")
                
                if char_to_send:
                    logger.debug(f"Writing '{char_to_send}' to serial port.")
                    self.serial_connection.write(char_to_send.encode('ascii'))

            else:
                logger.warning(f"Unknown motor command format: '{message}'")

        except (ValueError, IndexError) as e:
            logger.error(f"Invalid command format for message '{message}': {e}")
        except Exception as e:
            logger.error(f"Error handling command '{message}': {e}", exc_info=True)

    def start(self):
        """The main loop for the motor control process."""
        logger.info("Motor Control Process Started")
        while not self.shutdown_flag.is_set():
            try:
                message = self.motor_queue.get(timeout=1.0)
                
                if message == "shutdown":
                    logger.info("Shutdown signal received.")
                    self.shutdown_flag.set()
                    continue

                logger.debug(f"Received command from queue: '{message}'")
                self.handle_command(message)

            except multiprocessing.queues.Empty:
                continue
            except Exception as e:
                logger.error(f"Error in motor control loop: {e}", exc_info=True)
        
        self.cleanup()
        logger.info("Motor Control Shutting Down")


def motor_control_process(motor_queue, shutdown_flag):
    """The target function for the multiprocessing.Process."""
    setup_logging()
    logger.info("Setting up MotorController process.")
    motor_controller = MotorController(motor_queue)
    motor_controller.shutdown_flag = shutdown_flag
    motor_controller.start()

if __name__ == "__main__":
    setup_logging()
    logger.info("Testing Motor Control Process independently...")
    
    test_queue = multiprocessing.Queue()
    test_shutdown = multiprocessing.Event()
    
    motor_process = multiprocessing.Process(target=motor_control_process, args=(test_queue, test_shutdown))
    motor_process.start()
    
    print("\nSending 'turn_to:30' (should send 'R')")
    test_queue.put("turn_to:30")
    time.sleep(2)

    print("Sending 'turn_to:-45' (should send 'L')")
    test_queue.put("turn_to:-45")
    time.sleep(2)
    
    print("Sending 'turn_to:0' (should send 'C')")
    test_queue.put("turn_to:0")
    time.sleep(2)

    print("Sending shutdown signal.")
    test_shutdown.set()
    
    motor_process.join(timeout=5)
    if motor_process.is_alive():
        logger.warning("Process did not shut down cleanly, terminating.")
        motor_process.terminate()
        
    logger.info("Motor Control test complete.")
