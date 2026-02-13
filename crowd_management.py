import cv2
from picamera2 import Picamera2
import time
import numpy as np
import pyttsx3
import threading
import pyaudio
import wave
import argparse
from datetime import datetime
from collections import deque
from ultralytics import YOLO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AudioMonitor:
    """Monitor audio for coughing/sneezing sounds"""
    def __init__(self, threshold_db=40, chunk_size=1024):
        self.threshold_db = threshold_db
        self.chunk_size = chunk_size
        self.is_monitoring = False
        self.audio_events = deque(maxlen=10)
        self.p = pyaudio.PyAudio()
        
    def calculate_db(self, audio_data):
        """Calculate decibel level from audio data"""
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        if len(audio_array) == 0:
            return 0
        rms = np.sqrt(np.mean(audio_array**2))
        if rms > 0:
            db = 20 * np.log10(rms)
            return db
        return 0
    
    def detect_sudden_sound(self, audio_data):
        """Detect sudden loud sounds (potential cough/sneeze)"""
        db_level = self.calculate_db(audio_data)
        
        # Detect sudden sound above threshold
        if db_level > self.threshold_db:
            current_time = time.time()
            
            # Check if it's a new event (not part of recent event)
            if not self.audio_events or (current_time - self.audio_events[-1]) > 2.0:
                self.audio_events.append(current_time)
                logger.info(f"Sudden sound detected: {db_level:.1f} dB")
                return True
        
        return False
    
    def monitor_audio(self, callback):
        """Monitor audio in background thread"""
        try:
            stream = self.p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            logger.info("Audio monitoring started")
            
            while self.is_monitoring:
                try:
                    audio_data = stream.read(self.chunk_size, exception_on_overflow=False)
                    if self.detect_sudden_sound(audio_data):
                        callback()
                except Exception as e:
                    logger.error(f"Audio read error: {e}")
                    time.sleep(0.1)
            
            stream.stop_stream()
            stream.close()
            
        except Exception as e:
            logger.error(f"Audio monitoring error: {e}")
    
    def start(self, callback):
        """Start audio monitoring in background thread"""
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(
            target=self.monitor_audio, 
            args=(callback,), 
            daemon=True
        )
        self.monitor_thread.start()
    
    def stop(self):
        """Stop audio monitoring"""
        self.is_monitoring = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=2)
        self.p.terminate()


class CrowdManagementRobot:
    def __init__(self, camera_source=0, model_path='yolov8n.pt'):
        """
        Initialize the Crowd Management Robot
        
        Args:
            camera_source: Camera index or video file path (0 for default webcam)
            model_path: Path to YOLO model weights
        """
        # Camera setup
        logger.info("Initializing camera with Picamera2...")
        self.picam2 = Picamera2()
        config = self.picam2.create_preview_configuration(main={"size": (640, 480)})
        self.picam2.configure(config)
        self.picam2.start()
        time.sleep(1)  # Allow camera to warm up
        
        # Load YOLO model for person detection
        logger.info("Loading YOLO model...")
        self.model = YOLO(model_path)
        
        # Audio monitor for cough/sneeze detection
        try:
            self.audio_monitor = AudioMonitor(threshold_db=40)
            self.audio_enabled = True
            logger.info("Audio monitoring enabled")
        except Exception as e:
            logger.warning(f"Audio monitoring disabled: {e}")
            self.audio_monitor = None
            self.audio_enabled = False
        
        # Text-to-speech engine
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('voice', 'gmw/en-us')
        self.tts_engine.setProperty('rate', 150)  # Speed of speech
        self.tts_engine.setProperty('volume', 1.0)  # Volume level
        
        # Crowd management thresholds
        self.THRESHOLDS = {
            'low_crowd': 5,
            'medium_crowd': 15,
            'high_crowd': 25,
            'distance_threshold': 100,  # pixels - closer threshold for better detection
            'queue_cluster_size': 5,
            'close_distance_warning': 80  # Very close distance for immediate warning
        }
        
        # Safety messages
        self.MESSAGES = {
            'social_distance': "Attention! Please maintain safe distance from others.",
            'close_proximity': "Warning! You are too close to others. Please step back.",
            'wear_mask': "Please wear your mask properly for everyone's safety.",
            'cough_sneeze_detected': "Coughing or sneezing detected. Please wear your mask and use hand sanitizer.",
            'queue_forming': "Queue is forming. Please stand in line and maintain distance.",
            'overcrowding': "This area is crowded. Please move to less congested zones.",
            'general_safety': "For your safety, please follow the marked paths and maintain distance."
        }
        
        # Tracking variables
        self.crowd_count = 0
        self.crowd_density = 'low'
        self.last_announcement_time = {}
        self.announcement_cooldown = 8  # seconds between same announcements
        self.detection_history = deque(maxlen=30)  # Store last 30 frames
        
        # Running flag
        self.is_running = False
        self.announcement_queue = []
        self.lock = threading.Lock()
        
        # Audio event tracking
        self.last_audio_warning_time = 0
        self.audio_warning_cooldown = 15  # seconds between audio warnings
        
        logger.info("Crowd Management Robot initialized successfully")
    
    def on_audio_event_detected(self):
        """Callback for when cough/sneeze is detected"""
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_audio_warning_time > self.audio_warning_cooldown:
            with self.lock:
                self.announcement_queue.append(self.MESSAGES['cough_sneeze_detected'])
                self.announcement_queue.append(self.MESSAGES['wear_mask'])
            self.last_audio_warning_time = current_time
            logger.warning("Cough/sneeze detected - mask warning triggered")
    
    def detect_people(self, frame):
        """
        Detect people in the frame using YOLO
        
        Returns:
            list: List of detection boxes [x1, y1, x2, y2, confidence]
        """
        results = self.model(frame, classes=[0], verbose=False)  # class 0 is person
        detections = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                
                if confidence > 0.5:  # Confidence threshold
                    detections.append([x1, y1, x2, y2, confidence])
        
        return detections
    
    def calculate_centroids(self, detections):
        """Calculate center points of detected people"""
        centroids = []
        for det in detections:
            x1, y1, x2, y2 = det[:4]
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            centroids.append((cx, cy))
        return centroids
    
    def check_social_distancing(self, centroids):
        """
        Check if people are maintaining social distance
        
        Returns:
            tuple: (violations, critical_violations) - pairs of people violating distance
        """
        violations = []
        critical_violations = []
        
        for i in range(len(centroids)):
            for j in range(i + 1, len(centroids)):
                dist = np.sqrt((centroids[i][0] - centroids[j][0])**2 + 
                             (centroids[i][1] - centroids[j][1])**2)
                
                if dist < self.THRESHOLDS['close_distance_warning']:
                    critical_violations.append((i, j))
                    violations.append((i, j))
                elif dist < self.THRESHOLDS['distance_threshold']:
                    violations.append((i, j))
        
        return violations, critical_violations
    
    def detect_queue_formation(self, centroids):
        """
        Detect if people are forming queues (clustering)
        
        Returns:
            bool: True if queue detected
        """
        if len(centroids) < self.THRESHOLDS['queue_cluster_size']:
            return False
        
        # Simple clustering based on proximity
        clusters = []
        visited = set()
        
        for i, point in enumerate(centroids):
            if i in visited:
                continue
            
            cluster = [i]
            visited.add(i)
            
            for j, other_point in enumerate(centroids):
                if j in visited:
                    continue
                
                dist = np.sqrt((point[0] - other_point[0])**2 + 
                             (point[1] - other_point[1])**2)
                
                if dist < self.THRESHOLDS['distance_threshold'] * 1.5:
                    cluster.append(j)
                    visited.add(j)
            
            if len(cluster) >= self.THRESHOLDS['queue_cluster_size']:
                return True
        
        return False
    
    def analyze_crowd(self, detections, centroids):
        """
        Analyze crowd and determine what announcements to make
        
        Returns:
            list: Messages to announce
        """
        messages_to_announce = []
        current_time = time.time()
        
        # Update crowd count
        self.crowd_count = len(detections)
        
        # Determine crowd density
        if self.crowd_count < self.THRESHOLDS['low_crowd']:
            self.crowd_density = 'low'
        elif self.crowd_count < self.THRESHOLDS['medium_crowd']:
            self.crowd_density = 'medium'
        elif self.crowd_count < self.THRESHOLDS['high_crowd']:
            self.crowd_density = 'high'
        else:
            self.crowd_density = 'critical'
        
        # Check for overcrowding
        if self.crowd_count >= self.THRESHOLDS['high_crowd']:
            if self._can_announce('overcrowding', current_time):
                messages_to_announce.append(self.MESSAGES['overcrowding'])
                logger.warning(f"Overcrowding detected: {self.crowd_count} people")
        
        # Check social distancing
        violations, critical_violations = self.check_social_distancing(centroids)
        
        # Critical violations - people too close
        if len(critical_violations) > 0:
            if self._can_announce('close_proximity', current_time, cooldown=5):
                messages_to_announce.append(self.MESSAGES['close_proximity'])
                logger.warning(f"Critical proximity violations: {len(critical_violations)} pairs")
        
        # Regular violations
        elif len(violations) > 2:  # Multiple violations
            if self._can_announce('social_distance', current_time):
                messages_to_announce.append(self.MESSAGES['social_distance'])
                logger.warning(f"Social distancing violations: {len(violations)} pairs")
        
        # Check for queue formation
        if self.detect_queue_formation(centroids):
            if self._can_announce('queue_forming', current_time):
                messages_to_announce.append(self.MESSAGES['queue_forming'])
                logger.info("Queue formation detected")
        
        return messages_to_announce
    
    def _can_announce(self, message_type, current_time, cooldown=None):
        """Check if enough time has passed since last announcement of this type"""
        if cooldown is None:
            cooldown = self.announcement_cooldown
            
        if message_type not in self.last_announcement_time:
            self.last_announcement_time[message_type] = current_time
            return True
        
        if current_time - self.last_announcement_time[message_type] > cooldown:
            self.last_announcement_time[message_type] = current_time
            return True
        
        return False
     
    def make_announcement(self, message):
        """Make audio announcement using text-to-speech"""
        try:
            logger.info(f"🔊 Announcement: {message}")
            self.tts_engine.say(message)
            self.tts_engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS Error: {e}")
    
    def announcement_worker(self):
        """Worker thread for handling announcements"""
        while self.is_running:
            if self.announcement_queue:
                with self.lock:
                    if self.announcement_queue:
                        message = self.announcement_queue.pop(0)
                        self.make_announcement(message)
            time.sleep(0.1)
    
    def draw_detections(self, frame, detections, centroids, violations, critical_violations):
        """Draw bounding boxes and information on frame"""
        # Draw detections
        for i, det in enumerate(detections):
            x1, y1, x2, y2, conf = det
            color = (0, 255, 0)  # Green for normal
            
            # Check if this person is in critical violation
            for v in critical_violations:
                if i in v:
                    color = (0, 0, 255)  # Red for critical violation
                    break
            
            # Check if in regular violation
            if color == (0, 255, 0):
                for v in violations:
                    if i in v:
                        color = (0, 165, 255)  # Orange for regular violation
                        break
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.circle(frame, centroids[i], 5, color, -1)
            
            # Draw detection zone
            cv2.circle(frame, centroids[i], self.THRESHOLDS['distance_threshold'], 
                      (255, 255, 0), 1)
        
        # Draw critical violation lines (thicker, red)
        for v in critical_violations:
            pt1 = centroids[v[0]]
            pt2 = centroids[v[1]]
            cv2.line(frame, pt1, pt2, (0, 0, 255), 3)
            # Draw warning text
            mid_point = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2)
            cv2.putText(frame, "TOO CLOSE!", (mid_point[0] - 50, mid_point[1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        # Draw regular violation lines
        for v in violations:
            if v not in critical_violations:
                pt1 = centroids[v[0]]
                pt2 = centroids[v[1]]
                cv2.line(frame, pt1, pt2, (0, 165, 255), 2)
        
        # Draw info panel
        info_height = 160
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (450, info_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # Text info
        cv2.putText(frame, f"Crowd Count: {self.crowd_count}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Density: {self.crowd_density.upper()}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Distance Violations: {len(violations)}", (10, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Critical Violations: {len(critical_violations)}", (10, 120),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0) if len(critical_violations) > 0 else (255, 255, 255), 2)
        
        # Audio monitoring status
        audio_status = "ON" if self.audio_enabled else "OFF"
        audio_color = (0, 255, 0) if self.audio_enabled else (128, 128, 128)
        cv2.putText(frame, f"Audio Monitor: {audio_status}", (10, 150),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, audio_color, 2)
        
        # Status indicator
        if len(critical_violations) > 0:
            status_color = (0, 0, 255)  # Red
        elif len(violations) > 0:
            status_color = (0, 165, 255)  # Orange
        else:
            status_color = (0, 255, 0)  # Green
        
        cv2.circle(frame, (420, 30), 15, status_color, -1)
        
        return frame
    
    def run(self, display=True):
        """
        Main loop for crowd management system
        
        Args:
            display: If True, show video feed with detections
        """
        self.is_running = True
        
        # Start announcement worker thread
        announcement_thread = threading.Thread(target=self.announcement_worker, daemon=True)
        announcement_thread.start()
        
        # Start audio monitoring if enabled
        if self.audio_enabled and self.audio_monitor:
            self.audio_monitor.start(self.on_audio_event_detected)
        
        logger.info("=" * 60)
        logger.info("Crowd Management Robot started")
        logger.info("Features enabled:")
        logger.info("  ✓ Person detection and counting")
        logger.info("  ✓ Social distancing monitoring")
        logger.info("  ✓ Queue formation detection")
        logger.info(f"  {'✓' if self.audio_enabled else '✗'} Audio monitoring (cough/sneeze detection)")
        logger.info("Press 'q' to quit")
        logger.info("=" * 60)
        
        try:
            while self.is_running:
                frame = self.picam2.capture_array()
                if frame is None:
                    logger.error("Failed to read frame from camera")
                    break

                # Convert 4-channel RGBA image to 3-channel RGB
                if frame.shape[2] == 4:
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
                
                # Detect people
                detections = self.detect_people(frame)
                centroids = self.calculate_centroids(detections)
                
                # Analyze crowd
                messages = self.analyze_crowd(detections, centroids)
                
                # Queue announcements
                if messages:
                    with self.lock:
                        self.announcement_queue.extend(messages)
                
                # Check violations for visualization
                violations, critical_violations = self.check_social_distancing(centroids)
                
                # Draw on frame
                if display:
                    frame = self.draw_detections(frame, detections, centroids, 
                                                violations, critical_violations)
                    cv2.imshow('Crowd Management Robot', frame)
                
                # Handle key press
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    logger.info("Quit command received")
                    break
                
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        finally:
            self.stop()
    
    def stop(self):
        """Clean up resources"""
        logger.info("Shutting down...")
        self.is_running = False
        
        # Stop audio monitoring
        if self.audio_enabled and self.audio_monitor:
            self.audio_monitor.stop()
        
        if hasattr(self, 'picam2') and self.picam2.started:
            self.picam2.stop()
        cv2.destroyAllWindows()
        logger.info("Crowd Management Robot stopped")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Crowd Management Robot")
    parser.add_argument("--camera", type=str, default='0', help="Camera index or device path to use")
    args = parser.parse_args()

    print("=" * 60)
    print("  CROWD MANAGEMENT ROBOT")
    print("  Enhanced with Audio Monitoring")
    print("=" * 60)
    print()
    
    # Initialize robot with camera source
    camera_source = args.camera
    try:
        # Try converting to integer for camera index
        camera_source = int(camera_source)
    except ValueError:
        # Keep as string if it's a file path
        pass
    
    try:
        robot = CrowdManagementRobot(camera_source=camera_source)
        # Run the system with display
        robot.run(display=True)
    except RuntimeError as e:
        logger.error(f"Failed to initialize or run robot: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()