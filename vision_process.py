import cv2
from picamera2 import Picamera2
import time
import numpy as np
import multiprocessing
import argparse
from collections import deque
from ultralytics import YOLO
import logging
import os
from logging_config import setup_logging
from shared_state import STATE_IDLE

logger = logging.getLogger(__name__)

class VisionProcess:
    def __init__(self, audio_queue, shared_interaction_state, model_path='yolov8n.pt'):
        """
        Initialize the Vision & Monitoring Process.
        """
        self.audio_queue = audio_queue
        self.shared_interaction_state = shared_interaction_state
        self.initialization_failed = False
        
        try:
            logger.info("Initializing camera with Picamera2...")
            self.picam2 = Picamera2()
            # Explicitly request RGB888 format to ensure 3 channels for YOLO
            config = self.picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
            self.picam2.configure(config)
            self.picam2.start()
            logger.debug("Camera started, sleeping for 1 second for sensor to stabilize.")
            time.sleep(1)

            logger.info(f"Loading YOLO model from '{model_path}'...")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"YOLO model file not found at: {model_path}")
            self.model = YOLO(model_path)

        except Exception as e:
            logger.critical(f"CRITICAL: Vision process failed to initialize: {e}", exc_info=True)
            self.initialization_failed = True
            return

        self.THRESHOLDS = {
            'low_crowd': 5, 'medium_crowd': 15, 'high_crowd': 25,
            'distance_threshold': 100,
            'queue_cluster_size': 5,
            'close_distance_warning': 80
        }
        
        self.MESSAGES = {
            'social_distance': "social_distance.mp3",
            'close_proximity': "close_proximity.mp3",
            'wear_mask': "wear_mask.mp3",
            'cough_sneeze_detected': "cough_sneeze.mp3",
            'queue_forming': "queue_forming.mp3",
            'overcrowding': "overcrowding.mp3",
        }
        
        self.crowd_count = 0
        self.last_announcement_time = {}
        self.announcement_cooldown = 10
        self.shutdown_flag = multiprocessing.Event()
        logger.info("Vision Process initialized successfully")

    def detect_people(self, frame):
        """Detect people in the frame using YOLO."""
        logger.debug("Starting person detection on frame.")
        results = self.model(frame, classes=[0], verbose=False)
        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                if confidence > 0.5:
                    detections.append([x1, y1, x2, y2])
        logger.debug(f"Found {len(detections)} people.")
        return detections

    def calculate_centroids(self, detections):
        """Calculate center points of detected people."""
        return [((d[0] + d[2]) // 2, (d[1] + d[3]) // 2) for d in detections]

    def check_social_distancing(self, centroids):
        """Check for social distancing violations."""
        violations = []
        critical_violations = []
        for i in range(len(centroids)):
            for j in range(i + 1, len(centroids)):
                dist = np.linalg.norm(np.array(centroids[i]) - np.array(centroids[j]))
                if dist < self.THRESHOLDS['close_distance_warning']:
                    critical_violations.append((i, j))
                elif dist < self.THRESHOLDS['distance_threshold']:
                    violations.append((i, j))
        if violations or critical_violations:
            logger.debug(f"Distance check complete. Violations: {len(violations)}, Critical: {len(critical_violations)}")
        return violations, critical_violations

    def detect_queue_formation(self, centroids):
        if len(centroids) < self.THRESHOLDS['queue_cluster_size']:
            return False
        
        from scipy.cluster.hierarchy import linkage, fcluster
        if len(centroids) < 2: return False
        
        Z = linkage(centroids, method='single', metric='euclidean')
        clusters = fcluster(Z, self.THRESHOLDS['distance_threshold'], criterion='distance')
        
        unique, counts = np.unique(clusters, return_counts=True)
        if np.any(counts >= self.THRESHOLDS['queue_cluster_size']):
            logger.info(f"Potential queue detected. Cluster sizes: {counts}")
            return True
        return False

    def analyze_crowd(self, detections, centroids):
        """Analyze crowd and queue audio announcements."""
        current_time = time.time()
        self.crowd_count = len(detections)
        logger.debug(f"Analyzing crowd of size {self.crowd_count}.")

        if self.crowd_count >= self.THRESHOLDS['high_crowd']:
            if self._can_announce('overcrowding', current_time):
                self.queue_announcement(self.MESSAGES['overcrowding'])
                logger.warning(f"Overcrowding detected: {self.crowd_count} people")

        violations, critical_violations = self.check_social_distancing(centroids)
        if len(critical_violations) > 0:
            if self._can_announce('close_proximity', current_time, cooldown=5):
                self.queue_announcement(self.MESSAGES['close_proximity'])
                logger.warning(f"Critical proximity violations: {len(critical_violations)} pairs")
        elif len(violations) > 2:
            if self._can_announce('social_distance', current_time):
                self.queue_announcement(self.MESSAGES['social_distance'])
                logger.warning(f"Social distancing violations: {len(violations)} pairs")

        if self.detect_queue_formation(centroids):
            if self._can_announce('queue_forming', current_time):
                self.queue_announcement(self.MESSAGES['queue_forming'])
                logger.info("Queue formation detected and announced.")

    def _can_announce(self, msg_type, current_time, cooldown=None):
        cooldown = cooldown or self.announcement_cooldown
        last_time = self.last_announcement_time.get(msg_type, 0)
        can_announce = (current_time - last_time) > cooldown
        if can_announce:
            self.last_announcement_time[msg_type] = current_time
            logger.debug(f"Cooldown passed for announcement type '{msg_type}'. Can announce.")
        return can_announce

    def queue_announcement(self, message):
        # Check the global interaction state. Only make an announcement if the robot is idle.
        if self.shared_interaction_state.value != STATE_IDLE:
            logger.info(f"Vision: Deferring announcement '{message}' because robot is not in IDLE state (current state: {self.shared_interaction_state.value}).")
            return

        try:
            audio_request = {'command': 'play', 'file': message}
            logger.info(f"Vision: Queueing audio request '{audio_request}'")
            self.audio_queue.put(audio_request)
        except Exception as e:
            logger.error(f"Failed to queue announcement: {e}", exc_info=True)

    def draw_detections(self, frame, detections, centroids, violations, critical_violations):
        """Draws detections, centroids, and social distancing violations on the frame."""
        # Convert frame to BGR for OpenCV drawing functions (if not already)
        if frame.ndim == 3 and frame.shape[2] == 3: # Assuming RGB888 from Picamera2 config
            display_frame = frame # OpenCV can draw on RGB, but it expects BGR
        else:
            display_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR) # Fallback for grayscale, should not happen

        # Draw bounding boxes
        for i, (x1, y1, x2, y2) in enumerate(detections):
            color = (0, 255, 0) # Green for detected person
            cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(display_frame, f'Person {i+1}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Draw centroids
        for i, (cx, cy) in enumerate(centroids):
            cv2.circle(display_frame, (cx, cy), 5, (0, 0, 255), -1) # Red dot for centroid

        # Draw social distancing violations
        for i, j in violations:
            p1 = centroids[i]
            p2 = centroids[j]
            cv2.line(display_frame, p1, p2, (0, 255, 255), 2) # Yellow for regular violation

        for i, j in critical_violations:
            p1 = centroids[i]
            p2 = centroids[j]
            cv2.line(display_frame, p1, p2, (0, 0, 255), 2) # Red for critical violation

        # Display crowd count
        cv2.putText(display_frame, f'Crowd: {self.crowd_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        return display_frame

    def run(self, display=True):
        if self.initialization_failed:
            logger.error("Cannot start VisionProcess run loop because initialization failed.")
            return

        logger.info("Vision process run loop started.")
        try:
            while not self.shutdown_flag.is_set():
                logger.debug("Capturing frame...")
                try:
                    frame = self.picam2.capture_array()
                except Exception as e:
                    logger.error(f"Failed to capture frame from camera: {e}", exc_info=True)
                    time.sleep(2)
                    continue

                # Frame should already be RGB888 (3 channels) from configuration
                # No need for cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB) here anymore

                detections = self.detect_people(frame)
                centroids = self.calculate_centroids(detections)
                self.analyze_crowd(detections, centroids)

                # Cooldown logic to reduce CPU usage when idle
                if len(detections) == 0:
                    logger.debug("No people detected, sleeping for 1 second.")
                    time.sleep(1)
                
                if display:
                    violations, critical = self.check_social_distancing(centroids)
                    frame = self.draw_detections(frame, detections, centroids, violations, critical) # Uncommented and using the new method
                    cv2.imshow('Vision Process', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    logger.info("Quit command received from display window.")
                    break
        finally:
            self.stop()

    def stop(self):
        logger.info("Shutting down Vision Process...")
        if hasattr(self, 'picam2') and self.picam2.started:
            self.picam2.stop()
            logger.info("Camera stopped.")
        cv2.destroyAllWindows()
        logger.info("Vision Process stopped.")

def vision_process_func(audio_queue, shutdown_flag, shared_interaction_state):
    """Target function for the multiprocessing.Process."""
    setup_logging()
    logging.getLogger(__name__).setLevel(logging.WARNING)
    logger.info("Setting up VisionProcess.")
    vision_system = VisionProcess(audio_queue, shared_interaction_state)
    vision_system.shutdown_flag = shutdown_flag
    vision_system.run()

if __name__ == "__main__":
    setup_logging()
    logger.info("Testing Vision Process independently...")
    try:
        vision_proc = VisionProcess(multiprocessing.Queue(), multiprocessing.Value('i', STATE_IDLE)) 
        vision_proc.run()
    except KeyboardInterrupt:
        logger.info("Test stopped by user.")
    except Exception as e:
        logger.error(f"Error during independent test: {e}", exc_info=True)
    finally:
        logger.info("Vision Process test complete.")
