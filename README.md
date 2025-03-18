# AI Voice Assistant 

This is a **fully offline voice assistant** that continuously listens for voice input, responds intelligently, and can control home automation devices like lights and fans.  This is for a Hackathon which is being conducted by Jain Online

# My Details
#### name: Shrijith S Menon
#### USN: 23BTRCL022
#### Branch- B.Tech CSE-AIML

## ✨ Features  
✅ **Always Listening** – No wake word needed.  
✅ **Speech-to-Text (STT)** – Uses **Vosk** for offline speech recognition.  
✅ **Conversational AI** – Uses **DialoGPT-Large** for casual chat.  
✅ **Text-to-Speech (TTS)** – Uses **pyttsx3** for offline voice output.  
✅ **Home Automation** – Can control lights, fans, and temperature (simulated).  

---

## 🚀 Installation  

### 1️⃣ **Clone the Repository**  
```sh
git clone https://github.com/ShrijithSM/PyHackathon.git
```

### 2️⃣ **Install Dependencies**  
```sh
pip install -r requirements.txt
```

### 3️⃣ **Download Vosk Model**  
Download a Vosk model from [Vosk Models](https://alphacephei.com/vosk/models) and extract it inside the project folder. Example:  
```
voice-assistant/
│── model/   # Put Vosk model files here
│── main.py
│── requirements.txt
│── README.md
```
---

## 🎤 Usage  

Run the assistant:  
```sh
python app.py
```

### **Commands You Can Try:**  
🟢 "Turn on the lights."  
🟢 "Turn off the fan."  
🟢 "Set temperature to 22."  
🟢 "How's the weather today?"  
🟢 "Tell me a joke."  
🟢 "Who is your creator?"  

The assistant will listen, process commands, and respond in real-time!  

---

## 🛠️ Technologies Used  
- **Speech-to-Text (STT):** Vosk  
- **Conversational AI:** DialoGPT-Large (Hugging Face)  
- **Text-to-Speech (TTS):** pyttsx3  
- **Audio Processing:** sounddevice  

---

## 🔥 Future Improvements  
🔹 Add real home automation control (e.g., smart plugs, IoT devices).  
🔹 Improve chatbot responses with a fine-tuned model.  
🔹 Build a GUI/Web Interface for better interaction.  