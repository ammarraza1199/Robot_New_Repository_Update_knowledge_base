import os
import sys
import logging
import requests
import shutil
import speech_recognition as sr
import pyaudio
from dotenv import load_dotenv

# Configure logging for the health check
logger = logging.getLogger("system_check")

def check_internet():
    """Checks internet connectivity by pinging a reliable host."""
    try:
        # Check Google (for STT)
        requests.get("https://www.google.com", timeout=3)
        # Check Groq API endpoint
        requests.get("https://api.groq.com", timeout=3)
        logger.info("[PASS] Internet Connectivity")
        return True
    except requests.RequestException as e:
        logger.error(f"[FAIL] Internet Connectivity: {e}")
        return False

def check_microphone(target_names=["miniDSP", "USB"]):
    """Checks if a microphone matching the target names is available."""
    try:
        mics = sr.Microphone.list_microphone_names()
        found = False
        for mic in mics:
            for target in target_names:
                if target.lower() in mic.lower():
                    logger.info(f"[PASS] Microphone detected: {mic}")
                    found = True
                    break
            if found: break
        
        if not found:
            # Fallback warning instead of hard fail, as default mic might work
            logger.warning(f"[WARNING] Targeted microphone ({target_names}) not found. Available: {mics}")
            logger.info("[PASS] Microphone check (soft pass with warning)")
            return True 
        return True
    except Exception as e:
        logger.error(f"[FAIL] Microphone check: {e}")
        return False

def check_speaker():
    """Checks if PyAudio can initialize and access an output device."""
    p = None
    try:
        p = pyaudio.PyAudio()
        count = p.get_device_count()
        if count > 0:
            logger.info(f"[PASS] Speaker System (PyAudio initialized, {count} devices found)")
            return True
        else:
            logger.error("[FAIL] Speaker System: No audio devices found.")
            return False
    except Exception as e:
        logger.error(f"[FAIL] Speaker System: {e}")
        return False
    finally:
        if p: p.terminate()

def check_camera():
    """Checks if Picamera2 can be initialized (simulated check to avoid resource locking)."""
    # Note: Initializing Picamera2 here might lock it for the main process.
    # Instead, we check if the camera module is loaded or device exists.
    if os.path.exists("/dev/video0"):
        logger.info("[PASS] Camera Device (/dev/video0 found)")
        return True
    else:
        # Depending on setup, it might not be video0 (e.g. libcamera).
        # We'll try a soft import check.
        try:
            from picamera2 import Picamera2
            logger.info("[PASS] Camera Library (Picamera2 importable)")
            return True
        except ImportError:
            logger.error("[FAIL] Camera Library: Picamera2 not found.")
            return False

def check_files():
    """Checks existence of critical files."""
    required_files = [
        "hospital_knowledge_base.json",
        "yolov8n.pt",
        ".env"
    ]
    missing = []
    for f in required_files:
        if not os.path.exists(f):
            missing.append(f)
    
    if missing:
        logger.error(f"[FAIL] Missing critical files: {missing}")
        return False
    
    # Check API Key specifically
    load_dotenv()
    if not os.getenv("GROQ_API_KEY"):
        logger.error("[FAIL] GROQ_API_KEY missing in .env")
        return False
        
    logger.info("[PASS] Critical Files & Config")
    return True

def check_disk_space(min_gb=0.5):
    """Checks if there is enough free disk space."""
    try:
        total, used, free = shutil.disk_usage(".")
        free_gb = free / (2**30)
        if free_gb < min_gb:
            logger.warning(f"[WARNING] Low Disk Space: {free_gb:.2f} GB free")
            return True # Soft pass
        logger.info(f"[PASS] Disk Space ({free_gb:.2f} GB free)")
        return True
    except Exception as e:
        logger.error(f"[FAIL] Disk Space check: {e}")
        return False

def run_health_check():
    """Runs all system checks sequentially."""
    logger.info("Starting System Health Check...")
    
    checks = [
        check_files,
        check_internet,
        check_microphone,
        check_speaker,
        check_camera,
        check_disk_space
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
            # We continue running other checks to give a full report
            
    if all_passed:
        logger.info("System Health Check PASSED. Starting Robot...")
        return True
    else:
        logger.critical("System Health Check FAILED. Check logs for details.")
        return False

if __name__ == "__main__":
    # Allow running this script independently
    logging.basicConfig(level=logging.INFO)
    if run_health_check():
        sys.exit(0)
    else:
        sys.exit(1)
