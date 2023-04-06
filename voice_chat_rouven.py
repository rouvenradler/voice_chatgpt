import os
import io
import pyaudio
import wave
import openai
from google.cloud import speech
from google.cloud import texttospeech


def record_wav():
    form_1 = pyaudio.paInt16
    chans = 1
    samp_rate = 16000
    chunk = 4096
    record_secs = 3
    dev_index = 1
    wav_output_filename = 'input.wav'

    audio = pyaudio.PyAudio()

    # Create pyaudio stream.
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                        input_device_index = dev_index,input = True, \
                        frames_per_buffer=chunk)
    print("recording")
    frames = []

    # Loop through stream and append audio chunks to frame array.
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk)
        frames.append(data)

    print("finished recording")

    # Stop the stream, close it, and terminate the pyaudio instantiation.
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the audio frames as .wav file.
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()

    return


def speech_to_text(speech_file):
    # setting Google credential
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'codelabsdemo-382716-fa8f8502bb82.json'

    # create client instance
    client = speech.SpeechClient()

    with io.open(speech_file, "rb") as audio_file:
            content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="de-DE",
    )

    # Detects speech in the audio file
    response = client.recognize(request={"config": config, "audio": audio})
    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

    stt = ""
    for result in response.results:
        stt += result.alternatives[0].transcript

    return stt


def ask_chat_gpt(question):
    try:
        OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
        print('ENV environment variable exists')
    except KeyError:
        print('ENV environment variable does not exist')

    messages = [
        {"role": "system", "content": "You are a kind helpful assistant."}
    ]

    message = question
    if message:
        messages.append(
            {"role": "user", "content": message}
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

    reply = chat.choices[0].message.content
    messages.append({"role": "system", "content": reply})

    return reply


def text_to_speech(answer):
    # setting Google credential
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'codelabsdemo-382716-fa8f8502bb82.json'

    tts = answer

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


def main():
    # Get WAV from microphone.
    record_wav()

    # Convert audio into text.
    question = speech_to_text("input.wav")

    # Send text to ChatGPT.
    answer = ask_chat_gpt(question)

    # Convert ChatGPT response into audio.
    text_to_speech(answer)

    # Play audio of reponse.
    os.system("aplay result.wav")


if __name__ == "__main__":
    main()