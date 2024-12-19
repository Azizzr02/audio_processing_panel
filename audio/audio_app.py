import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os

# Function to classify audio
def classify_audio():
    audio_file_path = filedialog.askopenfilename(
        title="Select an audio file",
        filetypes=[("Audio Files", "*.wav;*.mp3;*.flac;*.ogg")]
    )
    if audio_file_path:
        try:
            # Run the audio classification script and capture output
            result = subprocess.run(
                ["python", "audio_classification.py", audio_file_path],
                capture_output=True,
                text=True,
                check=True
            )
            # Display the output in the result_text area
            result_text.delete("1.0", tk.END)  # Clear previous results
            result_text.insert(tk.END, result.stdout)  # Show the output
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e.stderr}")

# Function to record audio
def record_audio():
    seconds = 5  # You can adjust this duration
    try:
        subprocess.run(["python", "voice_recorder.py", str(seconds)], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred while recording: {e}")

# Function for text-to-speech
def text_to_speech():
    text = input_text.get("1.0", tk.END).strip()  # Get text from the input area
    if text:
        try:
            # Call the text-to-speech script with the text as an argument
            subprocess.run(["python", "text_to_speech.py", text], check=True)
            input_text.delete("1.0", tk.END)  # Clear the text area after processing
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Input Warning", "Please enter some text.")

# Create the main application window
root = tk.Tk()
root.title("Audio Control Panel")

# Create main frame
main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(padx=10, pady=10)

# Create a label
label = tk.Label(main_frame, text="Audio Control Panel", font=("Helvetica", 20, "bold"))
label.pack(pady=10)

# Text input for text-to-speech
input_text = tk.Text(main_frame, height=5, width=40, wrap=tk.WORD)
input_text.pack(pady=10)

# Create buttons
classify_button = tk.Button(main_frame, text="Audio Classification", command=classify_audio, width=20)
classify_button.pack(pady=5)

record_button = tk.Button(main_frame, text="Record Audio", command=record_audio, width=20)
record_button.pack(pady=5)

speak_button = tk.Button(main_frame, text="Convert to Speech", command=text_to_speech, width=20)
speak_button.pack(pady=5)

# Scrolled text area for classification results
result_text = scrolledtext.ScrolledText(main_frame, height=10, width=50, wrap=tk.WORD)
result_text.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()