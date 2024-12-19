# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("audio-classification", model="SavorSauce/music_genres_classification-finetuned-gtzan")