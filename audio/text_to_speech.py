import sys
from gtts import gTTS
import os

# Check if text is provided as a command-line argument
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No text provided. Please provide text as a command-line argument.")
        sys.exit(1)
    
    # Join all arguments to form the complete text
    text = ' '.join(sys.argv[1:])

    # Create a gTTS object
    tts = gTTS(text=text, lang='en')

    # Define the output audio file
    output_file = "output.mp3"

    # Remove the old audio file if it exists
    if os.path.exists(output_file):
        os.remove(output_file)

    # Save the new audio file
    tts.save(output_file)

    # Play the audio file
    # For Windows
    os.system(f"start {output_file}")  # Opens with the default player

    # For macOS
    # os.system(f"afplay {output_file}")

    # For Linux
    # os.system(f"mpg321 {output_file}")