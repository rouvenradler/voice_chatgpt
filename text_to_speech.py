import os
from google.cloud import texttospeech

# setting Google credential
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'codelabsdemo-382716-fa8f8502bb82.json'

tts = "Hallo, das ist mein zweites Sound Beispiel"

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
synthesis_input = texttospeech.SynthesisInput(text=tts)

# Build the voice request, select the language code ("en-US") and the ssml
voice = texttospeech.VoiceSelectionParams(
    language_code="de-DE", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# The response's audio_content is binary.
with open("result.wav", "wb") as out:
    # Write the response to the output file.
    out.write(response.audio_content)