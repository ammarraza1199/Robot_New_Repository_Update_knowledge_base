# Hospital Robot: End User Troubleshooting Guide

**Hardware Configuration:**
*   **Controller**: Raspberry Pi 5
*   **Microphone**: miniDSP USB Interface
*   **Speaker**: 8ohm Speaker connected via Audio Card
*   **Vision**: Picamera2 Module
*   **Motion**: Arduino (UART connection)

This guide helps operators identify and resolve common issues based on system logs and observed behavior.

---

## 1. Audio & Voice Input Issues (miniDSP)

### Error: "WARNING: Target microphone 'miniDSP' not found"
**Symptom**: The robot defaults to a different microphone or fails to hear commands clearly.
**Cause**: The verified "miniDSP" USB device is not detected by the system.
**Changes/Actions to Perform**:
1.  **Check Physical Connection**: Ensure the miniDSP USB cable is firmly connected to the Raspberry Pi 5 USB 3.0 (blue) port.
2.  **Re-enumerate USB**: Unplug and replug the device.
3.  **Verify System Recognition**:
    *   Run command: `lsusb`
    *   Look for "miniDSP" in the specific list.
4.  **Restart Service**: Restart the robot software to trigger a new device scan.

### Error: "CRITICAL: No input microphones found"
**Symptom**: The robot starts but immediately displays errors or shuts down.
**Cause**: The Audio Card or USB interface works for output but offers no input channels.
**Changes/Actions to Perform**:
1.  **Check Audio Card Drivers**: Ensure drivers for your specific Audio Card expansion board are loaded in `/boot/config.txt`.
2.  **Check Permissions**: Ensure the `pi` user is part of the `audio` group (`sudo usermod -a -G audio pi`).

---

## 2. Speaker & Output Issues (Audio Card)

### Error: "CRITICAL: No suitable output device found"
**Symptom**: Robot is silent even when responding.
**Cause**: The system cannot find a device supporting the required sample rates (48kHz/44.1kHz).
**Changes/Actions to Perform**:
1.  **Check Speaker Connection**: Verify the 8ohm speaker wiring to the Audio Card terminals.
2.  **Verify Audio Output Selection**:
    *   Right-click the Volume icon on the Raspberry Pi Desktop.
    *   Ensure the correct "Audio Card" or "USB Audio" is selected, not "HDMI".
3.  **Test Alsa**:
    *   Run: `speaker-test -c2 -t wav` to verify raw sound output.

---

## 3. Vision & Camera Issues

### Error: "Camera Initialization Failed" or "Picamera2 not detected"
**Symptom**: Robot operates (blind) or crashes on startup. Vision features (crowd detection) are inactive.
**Cause**: Ribbon cable loose or camera usage blocked by another process.
**Changes/Actions to Perform**:
1.  **Reseat Cable**: Power off the Pi 5. Release the clamp on the camera port and firmly re-seat the ribbon cable.
2.  **Check Interface**: Ensure `legacy camera` stack is disabled and `libcamera` is active (default on Pi 5).
3.  **Kill Blocking Processes**: Ensure no other script is using the camera.

---

## 4. Operational Errors

### Error: "FATAL: GROQ_API_KEY environment variable not set"
**Symptom**: Robot responds to navigation questions but fails on general queries ("I don't know").
**Cause**: The connection to the Llama 3.1 AI Brain is missing.
**Changes/Actions to Perform**:
1.  **Check `.env` file**: Open the `.env` file in the root directory.
2.  **Add Key**: Ensure line `GROQ_API_KEY="your_actual_key_here"` exists and is correct.

### Error: "ConnectionError" / "RequestTimeout" (Groq API)
**Symptom**: Long pauses after asking a complex question, followed by "Sorry, I'm having trouble connecting...".
**Cause**: No internet connection or weak Wi-Fi signal on the Raspberry Pi 5.
**Changes/Actions to Perform**:
1.  **Check Wi-Fi**: Ensure the Pi is connected to a stable network with 5GHz preference (supported by Pi 5).
2.  **Ping Test**: Run `ping 8.8.8.8` to verify connectivity.

---

## 5. Maintenance Checklist
*   **Daily**: Check `logs/robot_run.log` for "WARNING" or "CRITICAL" entries.
*   **Weekly**: Clean the microphone array (miniDSP) of dust to ensure clear voice capture.
*   **Monthly**: Backup user logs and clear old cache files in `audio_cache/` if storage is low.
