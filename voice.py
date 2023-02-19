import json, pyaudio
from vosk import Model, KaldiRecognizer

model_en, model_ru = Model('small_model_en_us'), Model('small_model_ru')
rec_en, rec_ru = KaldiRecognizer(model_en, 16000), KaldiRecognizer(model_ru, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec_en.AcceptWaveform(data) or rec_ru.AcceptWaveform(data)) and len(data) > 0:
            answer_en = json.loads(rec_en.Result())['text']
            answer_ru = json.loads(rec_ru.Result())['text']
            answer = {'en': answer_en, 'ru': answer_ru}
            yield answer


for text in listen():
    print(text)
