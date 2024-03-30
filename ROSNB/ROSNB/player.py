import pyaudio
import wave
from threading import Thread


class Music:

    def player(self):
        print("冲冲冲")
        wav = wave.Wave_read("/home/ucar/ucar_ws/src/nb/scripts/ROSNB/cfh.wav")
        p = pyaudio.PyAudio()
        s = p.open(wav.getframerate(), wav.getnchannels(),
                   pyaudio.get_format_from_width(wav.getsampwidth()), input=False, output=True)

        b = wav.readframes(512)
        while not b == b'':
            s.write(b)
            b = wav.readframes(512)
        p.close(s)
        p.terminate()
        wav.close()
        print("冲锋完毕")
