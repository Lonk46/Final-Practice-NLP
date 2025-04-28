import assemblyai as aai


import keyboard
import pyaudio
import wave
import time



# LOCAL SPEECH TO TEXT
# Audio parameters
FORMAT = pyaudio.paInt16     # 16-bit resolution
CHANNELS = 1                 # 1 channel for mono; change to 2 for stereo
RATE = 44100                 # 44.1kHz sample rate
CHUNK = 1024                 # 1024 samples per frame

audio = pyaudio.PyAudio()    # Create an interface to PortAudio

frames = []                  # To store recorded frames
recording = False            # Recording state flag


print("Press 'o' to start recording, 'p' to stop recording, and 'esc' to exit.")

while True:
    # Listen for the start recording key and ensure we aren't already recording
    if keyboard.is_pressed('o') and not recording:
        print("Recording started...")
        recording = True
        frames = []  # Reset the frames list

        # Open a new audio stream for recording
        stream = audio.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)
        
        # Give a short delay to avoid reading any leftover key presses
        time.sleep(0.5)

    # If recording, continuously read chunks from the microphone
    if recording:
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
        except Exception as e:
            print("Error during recording:", e)
            break

        # Check for the stop recording key
        if keyboard.is_pressed('p'):
            print("Recording stopped.")
            recording = False
            stream.stop_stream()
            stream.close()

            # Define a unique filename based on current timestamp
            #filename = f"recording_{int(time.time())}.wav"
            filename ="Recorded_audio.wav"
            waveFile = wave.open(filename, 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()
            print(f"Saved file as {filename}")

            # Small delay to avoid capturing the same key press multiple times
            time.sleep(0.5)

    # Allow exit from the loop if desired
    if keyboard.is_pressed('esc'):
        print("Exiting...")
        break

# Terminate the PortAudio interface
audio.terminate()



# SPEECH TO TEXT API --------------------------------------------------------
aai.settings.api_key = "7afd81bac73a4ff59019c310a62cd411"

# audio_file = "./local_file.mp3"
audio_file = r'C:\Users\Casa\Desktop\Procesamiento del lenguaje\Exam_practic_last\Recorded_audio.wav'

config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)

transcript = aai.Transcriber(config=config).transcribe(audio_file)

if transcript.status == "error":
  raise RuntimeError(f"Transcription failed: {transcript.error}")

transcribed_text = transcript.text
print(transcribed_text)


# TEXT TO SPEECH API ------------------------------------------------------

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import os
load_dotenv()
#client = ElevenLabs(
#  api_key=os.getenv("ELEVENLABS_API_KEY"),
#)
client = ElevenLabs(
  api_key="sk_a4885e47e373c030fc07f1adc43ee2718967aa1178dcbb0b",
)


audio = client.text_to_speech.convert(
    text=transcribed_text,
    voice_id="NOpBlnGInO9m6vDvFkFC",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)
play(audio)


