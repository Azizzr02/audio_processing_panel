from tkinter import *
from tkinter import ttk
import numpy as np
import scipy.signal as signal
import sounddevice as sd
import soundfile as sf
from tkinter import filedialog

window = Tk()

# Set up window properties
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 500
window_height = 500
x_window = int((screen_width - window_width) / 2)
y_window = int((screen_height - window_height) / 2)

window.geometry(f"{window_width}x{window_height}+{x_window}+{y_window}")
window.title("Equalizer")

# Equalizer bands and gain settings
bands = [(50, 150), (200, 400), (500, 1000), (1100, 2500), (3000, 6000), (6000, 10000)]
gains = [1, 1, 1, 1, 1, 1]
status = StringVar(window)
file_path = None
playClicked = False
audio_data = None
sr = None

def open_file():
    global file_path, audio_data, sr
    file_path = filedialog.askopenfilename(defaultextension=".wav",
                                           filetypes=[("Wave Files", "*.wav")])
    if file_path:
        status.set("File Loaded: " + file_path)
        audio_data, sr = sf.read(file_path)
        audio_data = audio_data.astype(np.float32)  # Ensure it is in the correct format

def start():
    global playClicked
    playClicked = True
    if audio_data is not None:
        apply_equalizer()  # Apply equalization before playing

def stop():
    sd.stop()
    status.set("Audio Paused")

def on_scale_changed(value):
    if playClicked:
        apply_equalizer()  # Apply equalization whenever a scale is changed

def apply_equalizer():
    global audio_data, sr
    if audio_data is None:
        return

    values = [scale.get() for scale in scales]
    order = 4
    filtered = np.zeros_like(audio_data)

    for i, band in enumerate(bands):
        f_low, f_high = band
        nyquist = 0.5 * sr
        low = f_low / nyquist
        high = f_high / nyquist

        b, a = signal.butter(order, [low, high], btype='bandpass')
        filtered += signal.lfilter(b, a, audio_data) * (10 ** (values[i] / 20))  # Apply gain

    # Normalize the filtered signal
    filtered /= np.max(np.abs(filtered))

    # Play the filtered audio
    sd.stop()  # Stop any currently playing audio to avoid overlap
    sd.play(filtered, sr)
    status.set("Playing filtered audio...")

# Create scales for each band
scales = []
for i in range(len(bands)):
    scale = Scale(window, from_=-12, to=12, orient=HORIZONTAL,
                  length=500, label="{}Hz - {}Hz".format(bands[i][0], bands[i][1]),
                  command=on_scale_changed)
    scale.set(gains[i])
    scale.pack()
    scales.append(scale)

# Add buttons
ttk.Button(window, text="Open File", command=open_file).pack(pady=5)
ttk.Button(window, text="Play", command=start).pack(pady=5)
ttk.Button(window, text="Stop", command=stop).pack(pady=5)

# Status label
ttk.Label(window, textvariable=status).pack(pady=10)

# Set initial status
status.set("Welcome to the Equalizer!")

window.mainloop()