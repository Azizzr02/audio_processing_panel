import librosa
from pedalboard.io import AudioFile
from pedalboard import *
import noisereduce as nr
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import librosa.display

# Define the sample rate
sr = 44100

# Load audio file
file_path = "111.wav"  # Replace with your actual file path
y, sr = librosa.load(file_path)

# Save original audio for playback
sf.write('original_audio.wav', y, sr)

# Load audio with Pedalboard
with AudioFile(file_path).resampled_to(sr) as f:
    audio = f.read(f.frames)

# Function to plot the spectrum
def plot_spectrum(y, sr, title):
    plt.figure(figsize=(10, 4))
    # Use only one channel for plotting
    if y.ndim > 1:
        y = np.mean(y, axis=0)  # Convert to mono if stereo
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log', cmap='coolwarm')
    plt.colorbar(format='%+2.0f dB')
    plt.title(title)
    plt.tight_layout()
    plt.show()

# Plot the original audio spectrum
plot_spectrum(audio, sr, 'Original Audio Spectrum')

# Aggressive noise reduction
reduced_noise = nr.reduce_noise(y=audio, sr=sr, stationary=False, prop_decrease=1.0)

# Applying audio effects to enhance clarity and remove hiss
board = Pedalboard([
    NoiseGate(threshold_db=-70, ratio=10.0, release_ms=250),  # More aggressive noise gating
    Compressor(threshold_db=-40, ratio=4.0),  # Moderate compression
    LowShelfFilter(cutoff_frequency_hz=300, gain_db=3, q=1),  # Boost low frequencies for warmth
    HighShelfFilter(cutoff_frequency_hz=4000, gain_db=-6, q=1),  # Cut high frequencies to reduce hiss
    LowShelfFilter(cutoff_frequency_hz=80, gain_db=-15, q=1),  # Aggressive cut for low rumble
    HighShelfFilter(cutoff_frequency_hz=1000, gain_db=-10, q=1),  # Reducing frequencies above 1000 Hz
    LowShelfFilter(cutoff_frequency_hz=2000, gain_db=-10, q=1),  # Reducing frequencies above 2000 Hz
    Gain(gain_db=7)  # Boost overall volume
])

# Process audio with effects
effected = board(reduced_noise, sr)

# Plot the enhanced audio spectrum
plot_spectrum(effected, sr, 'Enhanced Audio Spectrum')

# Debugging prints
print("Effected type:", type(effected))
print("Effected shape:", effected.shape)
print("Effected dtype:", effected.dtype)

# Normalize audio data if necessary
if isinstance(effected, np.ndarray):
    max_val = np.max(np.abs(effected))
    if max_val > 0:
        effected = (effected / max_val).astype(np.float32)

    # Save enhanced audio in WAV format
    output_file_path = 'enhanced_audio.wav'
    sf.write(output_file_path, effected.T, sr)  # Transpose for correct shape
else:
    print("Effected audio is not a valid NumPy array.")