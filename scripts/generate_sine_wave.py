import wave
import struct
import math

# Parameters
frequency = 440  # Hz (A4 note)
duration = 3     # seconds
sample_rate = 44100 # Hz
amplitude = 32000 # Max amplitude for 16-bit audio
filename = "test_sine.wav"

# Generate sine wave data
num_samples = int(sample_rate * duration)
wav_file = wave.open(filename, 'w')
wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed')) # 1 channel, 2 bytes per sample (16-bit)

for i in range(num_samples):
    value = int(amplitude * math.sin(2 * math.pi * frequency * i / sample_rate))
    wav_file.writeframes(struct.pack('<h', value)) # '<h' for signed short (16-bit)

wav_file.close()
print(f"Generated {filename}")
