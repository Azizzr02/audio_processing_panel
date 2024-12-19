import tkinter as tk
from tkinter import filedialog
import librosa
import numpy as np
from transformers import pipeline

# Set up the Tkinter root window (it won't be shown)
root = tk.Tk()
root.withdraw()  # Hide the root window

# Ask the user to select an audio file
audio_file_path = filedialog.askopenfilename(
    title="Select an audio file",
    filetypes=[("Audio Files", "*.wav;*.mp3;*.flac;*.ogg")]
)

# Check if a file was selected
if audio_file_path:
    # Load the audio file using librosa
    audio_input, sampling_rate = librosa.load(audio_file_path, sr=16000)  # Resampling to 16kHz

    # Use the pipeline for audio classification with the local model
    pipe = pipeline("audio-classification", model="SavorSauce/music_genres_classification-finetuned-gtzan")

    # Classify the audio input
    results = pipe(audio_input)

    # Display the results
    for result in results:
        print(f"Predicted Genre: {result['label']}, Score: {result['score']:.4f}")
else:
    print("No file selected.")