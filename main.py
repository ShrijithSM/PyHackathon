import queue
import sounddevice as sd
import vosk
import json
import pyttsx3
from transformers import AutoModelForCausalLM, AutoTokenizer

# Initialize Vosk for Speech-to-Text
model = vosk.Model("vosk-model-small-en-us-0.15")  # Change to your model path
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    q.put(bytes(indata))

# Initialize DialoGPT for Chatbot Responses
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model_chatbot = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

# Initialize Text-to-Speech (TTS)
engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def chatbot_response(text):
    """Generate response using DialoGPT."""
    inputs = tokenizer.encode(text + tokenizer.eos_token, return_tensors="pt")
    response_ids = model_chatbot.generate(
        inputs,
        max_length=100,
        pad_token_id=tokenizer.eos_token_id  # Suppress warning
    )
    return tokenizer.decode(response_ids[:, inputs.shape[-1]:][0], skip_special_tokens=True)

def process_command(text):
    """Process voice commands."""
    text = text.lower()
    
    print(f"User: {text}")  # Display what the user says

    if "turn on the lights" in text:
        response = "Turning on the lights."
    elif "turn off the lights" in text:
        response = "Turning off the lights."
    elif "open youtube" in text:
        response = "Opening YouTube."
    else:
        response = chatbot_response(text)  # If no command found, use chatbot

    print(f"Bot: {response}")  # Display bot's response
    speak(response)

# Start Listening for Voice Input
print("Listening... Speak now.")
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16",
                       channels=1, callback=callback):
    rec = vosk.KaldiRecognizer(model, 16000)

    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "")

            if text:
                process_command(text)  # Process the spoken text
