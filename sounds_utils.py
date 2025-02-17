import os
from playsound import playsound

def get_available_sounds(directory="Sounds"):
    if not os.path.exists(directory):
        return []
    return [f for f in os.listdir(directory) if f.endswith(".wav")]

def play_sound(sound_file_path):
    if os.path.exists(sound_file_path):
        playsound(sound_file_path)
