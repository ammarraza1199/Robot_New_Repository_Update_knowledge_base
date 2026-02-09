import wave
import struct
import math

# Parameters
frequency = 440  # Hz (A4 note)
duration = 3     # seconds
sample_rate = 44100 # Hz
amplitude = 32000 # Max amplitude for 16-bit audio
channels = 2     # STEREO
filename = "test_stereo_sine.wav"

# Generate sine wave data
num_samples = int(sample_rate * duration)
wav_file = wave.open(filename, 'w')
wav_file.setparams((channels, 2, sample_rate, num_samples, 'NONE', 'not compressed')) # 2 channels, 2 bytes per sample (16-bit)

for i in range(num_samples):
    value = int(amplitude * math.sin(2 * math.pi * frequency * i / sample_rate))
    # Write same value for both channels for a simple stereo tone
    wav_file.writeframes(struct.pack('<hh', value, value)) # '<hh' for two signed shorts (16-bit)

wav_file.close()
print(f"Generated {filename}")
