import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import os
import webbrowser as wb
import google.generativeai as genai
import requests
import json

# Optional: Offline speech recognition (Vosk)
try:
    from vosk import Model, KaldiRecognizer
    import pyaudio
    vosk_model = Model(r"D:\\SAI\\AI_VOICE\\vosk-model-small-en-in-0.4")  # Replace with your extracted Vosk model path
    use_vosk = True
except Exception as e:
    print("Vosk not available:", e)
    use_vosk = False

# Configure Gemini
genai.configure(api_key="YOUR_GEMINI_API_KEY")  # Replace with your Gemini API key

# Check if connected to internet
def is_online():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except requests.RequestException:
        return False

websites = {
    "youtube": "https://www.youtube.com", "google": "https://www.google.com",
    "code": "https://leetcode.com", "geeksforgeeks": "https://www.geeksforgeeks.org",
    "linked in": "https://www.linkedin.com", "github": "https://github.com",
    "stack overflow": "https://stackoverflow.com", "gmail": "https://mail.google.com",
    "chatgpt": "https://chat.openai.com", "coursera": "https://www.coursera.org",
    "udemy": "https://www.udemy.com", "nptel": "https://nptel.ac.in",
    "anurag": "https://anurag.edu.in", "moodle": "https://moodle.org",
    "google classroom": "https://classroom.google.com", "code forces": "https://codeforces.com",
    "code chef": "https://www.codechef.com", "hacker rank": "https://www.hackerrank.com",
    "hacker earth": "https://www.hackerearth.com", "notion": "https://www.notion.so",
    "drive": "https://drive.google.com", "spotify": "https://www.spotify.com",
    "netflix": "https://www.netflix.com", "instagram": "https://www.instagram.com"
}

folders = {
    "anime": "D:/SAI/Anime/op",
    "movies": "D:/SAI/Movies",
    "games":"D:/SAI/Games"
}

def replyAI(query):
    if is_online():
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            prompt = "Answer this as if you're a laptop assistant. Be short and clean: " + query
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print("Gemini API error:", e)
            return "Gemini is currently unreachable."
    else:
        return query_ollama(query)

def query_ollama(query):
    try:
        query = "Answer this as if you're a laptop assistant. Be short and clean: " + query
        ollama_prompt = {"model": "llama2-uncensored", "prompt": query}
        response = requests.post("http://localhost:11434/api/generate", json=ollama_prompt, stream=True)

        # Collect the response from the JSON lines
        final_response = ""
        for line in response.iter_lines():
            if line:
                data = line.decode('utf-8')
                try:
                    json_data = json.loads(data)
                    final_response += json_data.get("response", "")
                except Exception as parse_err:
                    print("JSON parse error:", parse_err)

        return final_response if final_response else "No response from Ollama."

    except Exception as e:
        print("Ollama error:", e)
        return "Offline mode failed."


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    print("Buddy:", text)
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    greet = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 18 else "Good Evening"
    speak(f"{greet}! I am Buddy. How can I help you today?")

# 🎤 Offline + Online Hybrid Speech Recognizer
def takeCommand():
    if (not is_online()) and use_vosk:
        try:
            rec = KaldiRecognizer(vosk_model, 16000)
            mic = pyaudio.PyAudio()
            stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
            stream.start_stream()
            print("Listening (offline)...")
            while True:
                data = stream.read(4000, exception_on_overflow=False)
                
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    query = result.get("text", "").strip()
                    stream.stop_stream()
                    return query.lower()
        except Exception as e:
            print("Vosk failed:", e)

    # fallback to Google Speech Recognition
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening (online)...")
            r.pause_threshold = 1
            audio = r.listen(source)
        print("Recognizing...")
        return r.recognize_google(audio, language='en-in').lower()
    except Exception:
        print("Didn't catch that.")
        return "none"

# 🧠 Main loop
if __name__ == "__main__":
    wishMe()

    while True:
        query = input("You: ").lower()  # For testing without voice input
        # query = takeCommand()  # Uncomment for voice inputh
        if query in ["none", ""]:
            continue
        print("User:", query)
        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            try:
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
            except Exception:
                speak("No results found.")

        elif 'use ai' in query or 'use artificial intelligence' in query:
            speak(replyAI(query))

        elif 'open' in query:
            for keyword, url in websites.items():
                if f"open {keyword}" in query:
                    speak(f"Opening {keyword}")
                    wb.open(url)
                    break
            for keyword,path in folders.items():
                if f"open {keyword}" in query:
                    speak(f"Opening {keyword}")
                    os.startfile(path)
                    break

        elif 'play music' in query:
            music_path = "D:\\SAI\\Music\\People X Nainowale Ne - Chillout Mashup - @YashrajMukhateOfficial  - MEHER.mp3"
            os.startfile(music_path)

        elif 'shutdown' in query:
            speak("Shutting down the system.")
            os.system("shutdown /s /t 1")
            break

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'exit' in query or 'quit' in query or 'bye' in query:
            speak("Goodbye! Have a great day!")
            break

        else:
            speak(replyAI(query))
