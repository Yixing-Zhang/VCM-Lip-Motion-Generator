import pyaudio
import numpy as np

CHUNK = 1470
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
while True:
    data = stream.read(CHUNK)
    # print(data[0:4])
    # print(len(data))
    decode = np.frombuffer(data, 'int16')

    print(decode)
