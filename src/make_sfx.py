import os
import math
import struct
import wave

# Create sfx directory
os.makedirs("sfx", exist_ok=True)

SAMPLE_RATE = 44100

def write_wav(filename: str, samples: list[float], sample_rate=SAMPLE_RATE):
    """Write mono 16-bit PCM WAV file."""
    path = os.path.join("sfx", filename)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        
        packed_bytes = bytearray()
        for s in samples:
            # Clamp sample to [-1.0, 1.0]
            val = max(-1.0, min(1.0, s))
            int_val = int(val * 32767.0)
            packed_bytes.extend(struct.pack("<h", int_val))
        wf.writeframes(packed_bytes)
    print(f"Generated: {path}")

# 1. Click SFX (Crisp pop)
def gen_click():
    duration = 0.06  # 60ms
    num_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 80.0)
        freq = 900.0 - (t / duration) * 400.0
        s = math.sin(2.0 * math.pi * freq * t) * env
        samples.append(s * 0.85)
    write_wav("click.wav", samples)

# 2. Compare SFX (Crisp double tick)
def gen_compare():
    duration = 0.08  # 80ms
    num_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 60.0)
        freq = 750.0 if t < 0.035 else 1050.0
        s = math.sin(2.0 * math.pi * freq * t) * env
        samples.append(s * 0.8)
    write_wav("compare.wav", samples)

# 3. Swap SFX (Audible sliding swoosh)
def gen_swap():
    duration = 0.25  # 250ms
    num_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        # Envelope: smooth parabolic envelope
        env = math.sin(math.pi * (t / duration)) ** 1.2
        # Frequency sweep from 220Hz to 650Hz
        freq = 220.0 + (t / duration) * 430.0
        # Add harmonic for richness
        s = 0.7 * math.sin(2.0 * math.pi * freq * t) + 0.3 * math.sin(4.0 * math.pi * freq * t)
        samples.append(s * env * 0.9)
    write_wav("swap.wav", samples)

# 4. Success SFX (Bright Major Chime C5 + E5 + G5 + C6)
def gen_success():
    duration = 0.5  # 500ms
    num_samples = int(SAMPLE_RATE * duration)
    samples = []
    freqs = [523.25, 659.25, 783.99, 1046.50]  # C Major chord
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 6.0)  # Bell decay
        s = sum(math.sin(2.0 * math.pi * f * t) for f in freqs) / len(freqs)
        samples.append(s * env * 0.95)
    write_wav("success.wav", samples)

if __name__ == "__main__":
    gen_click()
    gen_compare()
    gen_swap()
    gen_success()
