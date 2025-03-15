import queue
import sounddevice as sd
import vosk
import json
import pyttsx3
from transformers import AutoModelForCausalLM, AutoTokenizer

# Initialize Vosk model for speech recognition
vosk_model = vosk.Model("model")  # Path to your Vosk model folder
recognizer = vosk.KaldiRecognizer(vosk_model, 16000)

# Initialize Text-to-Speech (TTS) engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # Adjust speed
engine.setProperty('voice', engine.getProperty('voices')[1].id)  # Female voice

# Load DialoGPT for chatbot responses
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")

# Queue for audio data
audio_queue = queue.Queue()

# Home automation dummy functions
def control_lights(action):
    return f"Turning lights {action}."

def control_fan(action):
    return f"Turning fan {action}."

def set_temperature(temp):
    return f"Setting temperature to {temp}°C."

# Function to process voice commands
def process_command(text):
    text = text.lower()
    
    # Home automation commands
    if "turn on the light" in text or "lights on" in text:
        return control_lights("on")
    elif "turn off the light" in text or "lights off" in text:
        return control_lights("off")
    elif "turn on the fan" in text or "fan on" in text:
        return control_fan("on")
    elif "turn off the fan" in text or "fan off" in text:
        return control_fan("off")
    elif "set temperature to" in text:
        temp = ''.join(filter(str.isdigit, text))  # Extract numbers
        return set_temperature(temp)
    
    # Casual conversation using AI
    return chat_with_ai(text)

# Function to handle casual conversation using DialoGPT
def chat_with_ai(user_input):
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
    response_ids = model.generate(input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response

# Function to recognize speech
def recognize_speech():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=lambda indata, frames, time, status: audio_queue.put(bytes(indata))):
        print("Listening...")
        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())["text"]
                if result:
                    return result

# Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Main loop
def main():
    print("Voice Assistant is running... Always listening.")
    
    while True:
        user_input = recognize_speech()  # Convert speech to text
        print(f"\nUser: {user_input}")
        
        response = process_command(user_input)  # Process input
        print(f"Bot: {response}")

        speak(response)  # Speak response

if __name__ == "__main__":
    main()
