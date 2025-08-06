import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer
import os
import psutil  # NEW: to check if Buddy is running
import time

# Constants
BUDDY_SCRIPT_PATH = "YOUR_BUDDY.py PATH"
PYTHON_PATH = "YOUR_PYTHON_PATH"
MODEL_PATH = "YOUR vosk-model-small-en-us-0.15 PATH"
HOTWORD = "hey buddy"

# Load Vosk model
model = Model(MODEL_PATH)
rec = KaldiRecognizer(model, 16000)
q = queue.Queue()

# Microphone callback
def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# Function to check if Buddy.py is running
def is_buddy_running():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and 'Buddy.py' in proc.info['cmdline']:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

# Main loop
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    print("Buddy_starter is running. Waiting for hotword: 'hey buddy'...")

    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = rec.Result()
            text = json.loads(result)["text"]
            print("Heard:", text)

            if HOTWORD in text.lower():
                if not is_buddy_running():
                    print("Hotword detected and Buddy is not running. Launching Buddy...")
                    os.system(f'start "" "{PYTHON_PATH}" "{BUDDY_SCRIPT_PATH}"')

                else:
                    print("Buddy is already running.")
            time.sleep(1)  # Optional: prevent rapid re-triggers
