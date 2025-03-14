import asyncio

from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import silero
from api import AssistantFnc

import whisper
from transformers import AutoModelForCausalLM, AutoTokenizer
from TTS.api import TTS

load_dotenv()

# Load Whisper STT
whisper_model = whisper.load_model("small")  # Can be "base", "medium", or "large"

# Load Mistral LLM
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")

# Load Coqui TTS
tts = TTS(model_name="tts_models/en/ljspeech/glow-tts").to("cpu")


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a voice assistant created by LiveKit. Your interface with users will be voice. "
            "You should use short and concise responses, avoiding unpronounceable punctuation."
        ),
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    fnc_ctx = AssistantFnc()

    class FreeVoiceAssistant(VoiceAssistant):
        async def transcribe(self, audio_path):
            """Convert speech to text using Whisper."""
            result = whisper_model.transcribe(audio_path)
            return result["text"]

        async def generate_response(self, text):
            """Generate response using Mistral LLM."""
            inputs = tokenizer(text, return_tensors="pt")
            output = model.generate(**inputs, max_length=100)
            return tokenizer.decode(output[0], skip_special_tokens=True)

        async def synthesize_speech(self, text):
            """Convert text to speech using Coqui TTS."""
            tts.tts_to_file(text=text, file_path="response.wav")
            return "response.wav"

    assistant = FreeVoiceAssistant(
        vad=silero.VAD.load(),
        stt=None,  # Using custom Whisper function
        llm=None,  # Using custom Mistral function
        tts=None,  # Using custom Coqui function
        chat_ctx=initial_ctx,
        fnc_ctx=fnc_ctx,
    )
    assistant.start(ctx.room)

    await asyncio.sleep(1)
    await assistant.say("Hey, how can I help you today!", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
