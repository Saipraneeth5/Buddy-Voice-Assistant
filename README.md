# 🧠 Buddy - Voice Assistant with AI Support

**Buddy** is a personal desktop voice assistant that leverages both online and offline capabilities to interact with users using voice commands. It supports Gemini (Google Generative AI), Wikipedia search, system operations, website launching, and more — all via your voice.

---

## 🔧 Features

- 🎤 Voice command input (online using Google Speech API and offline using Vosk)
- 🧠 AI responses using Gemini API (fallback to Ollama offline model)
- 🌐 Open common websites & folders
- 🎬 Play media from your system
- 📚 Search summaries from Wikipedia
- ⏰ Time reporting
- 🔌 System operations (shutdown, exit)
- 🗣️ Text-to-Speech responses using `pyttsx3`

---

## 📁 Project Structure

```
├── Buddy.py             # Main assistant logic
├── buddy_starter.py     # Listens for the hotword "Hey Buddy" and launches assistant
├── requirements.txt     # Dependencies list
```

---

## 🖥️ Requirements

- Python 3.7+
- [Vosk model](https://alphacephei.com/vosk/models) (for offline voice recognition)
- Gemini API Key (if using Google Generative AI)
- Optional: [Ollama](https://ollama.com/) for offline LLM responses

---

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Buddy-Voice-Assistant.git
   cd Buddy-Voice-Assistant
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download and set up Vosk model**:
   - Download a model (e.g., `vosk-model-small-en-in-0.4`)
   - Extract it and update the path in `Buddy.py` and `buddy_starter.py`

4. **Edit paths**:
   - In `buddy_starter.py`, update:
     ```python
     BUDDY_SCRIPT_PATH = "path/to/Buddy.py"
     PYTHON_PATH = "path/to/python.exe"
     MODEL_PATH = "path/to/vosk-model-directory"
     ```

5. **(Optional) Configure Gemini**:
   - Replace `"YOUR_GEMINI_API_KEY"` in `Buddy.py` with your actual API key.

---

## 🚀 Usage

- Run `buddy_starter.py` to start hotword detection:
  ```bash
  python buddy_starter.py
  ```
- Say **"Hey Buddy"** to activate the assistant.
- You can also directly run:
  ```bash
  python Buddy.py
  ```

---

## 🧠 Example Commands

- `"Open YouTube"` – launches YouTube
- `"Play music"` – plays a specific song
- `"Search Elon Musk on Wikipedia"` – gives a short summary
- `"What is the time?"` – tells current time
- `"Use AI to explain quantum physics"` – fetches from Gemini or Ollama

---

## ✅ To Do

- Add GUI interface
- Add more offline fallback capabilities
- Enhance context awareness

---

## 📜 License

MIT License © 2025 Baira Sai Praneeth

---

## 💡 Credits

- [Vosk API](https://alphacephei.com/vosk/)
- [Google Gemini](https://ai.google.dev/)
- [Ollama](https://ollama.com/)

---