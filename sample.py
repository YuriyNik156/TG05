import wave
import os

def create_silent_ogg(filename="sample.ogg", duration_sec=2):
    wav_name = "temp.wav"
    # Создаём WAV с тишиной
    with wave.open(wav_name, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)     # 16 бит
        wf.setframerate(44100)
        wf.writeframes(b"\x00\x00" * 44100 * duration_sec)

    # Просто переименуем WAV в .ogg как заглушку
    os.rename(wav_name, filename)
    print(f"Файл {filename} создан!")

create_silent_ogg()
