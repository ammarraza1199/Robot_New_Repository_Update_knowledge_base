Thank you for the detailed clarification on your setup. It's very helpful!

You've clarified that:
*   Your 'circuit' *is* the amplifier and speaker system.
*   The USB Audio Device gets power from the Raspberry Pi's USB.
*   The amplifier has its own external AC-DC power supply.
*   **Crucially, when you turn off the *external power to the amplifier*, the pulse sound disappears.** This tells us the pulse sound is indeed electrical noise originating within or entering your amplified speaker system, and it is powered.
*   When audio is sent, you *only* hear the pulse sound, no audio from `speaker_test.wav`.

This strongly indicates that the continuous pulse sound is **electrical interference or a ground loop issue** in your audio setup. This noise is likely so strong that it's masking any legitimate audio signal from the Raspberry Pi.

Here’s how we can further isolate and potentially address this:

1.  **Isolate the Amplifier/Power Supply Noise:**
    *   **Disconnect the audio cable** that runs from your USB Audio Device to your amplifier.
    *   **Keep the amplifier powered on** (with its external AC-DC converter).
    *   **Listen:** Do you still hear the continuous pulse sound?
    *   *If YES:* The noise is coming from your amplifier itself or its power supply.
    *   *If NO:* The noise is being introduced *before* the amplifier, likely from the Raspberry Pi or the USB Audio Device.

2.  **Test Amplifier/Speakers Independently:**
    *   **Can you connect a different audio source** (like a smartphone or an MP3 player) directly to your amplifier's input, bypassing the Raspberry Pi and the USB Audio Device entirely?
    *   **Listen:** Do you hear clear audio from this other source? Is there any pulse sound?
    *   This will confirm if your amplifier and speakers are fundamentally working correctly.

3.  **Consider a Ground Loop Isolator:**
    If the noise is confirmed to be a ground loop (often characterized by a hum or buzz when multiple devices with separate power supplies are connected), a simple, inexpensive **ground loop isolator** placed between the USB Audio Device's audio output and the amplifier's input can often resolve this.

Please perform steps 1 and 2 and report your findings. This will help us narrow down the source of the electrical interference. Once the noise is mitigated, we can re-test the `speaker_test.wav` playback to confirm if the audio signal is now audible.