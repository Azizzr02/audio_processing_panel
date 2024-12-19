import sounddevice as sd
from scipy.io.wavfile import write
import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt

# Function to record audio
def record_audio():
    fs = 44100  # Sample rate
    seconds = 5  # Duration of recording

    print("Recording...")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished

    # Open file dialog to choose save location
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.asksaveasfilename(defaultextension=".wav",
                                             filetypes=[("WAV files", "*.wav")],
                                             title="Save recording as")
    if file_path:
        write(file_path, fs, myrecording)  # Save as WAV file
        print(f"Recording saved as {file_path}")
        return myrecording, fs
    else:
        print("Save operation cancelled.")
        return None, None

# Function to plot the spectrum of the recorded audio
def plot_spectrum(audio, fs):
    if audio is not None:
        # Compute the Fourier Transform of the audio signal
        n = len(audio)
        audio_fft = np.fft.fft(audio.flatten())
        audio_fft = np.abs(audio_fft[:n // 2]) * (2 / n)
        freqs = np.fft.fftfreq(n, 1 / fs)[:n // 2]

        # Plot the spectrum
        plt.figure(figsize=(10, 6))
        plt.plot(freqs, audio_fft)
        plt.title('Spectrum of Recorded Audio')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
        plt.grid()
        plt.show()
    else:
        print("No audio data to plot.")

# Run the functions
if __name__ == "__main__":
    audio_data, sample_rate = record_audio()
    plot_spectrum(audio_data, sample_rate)