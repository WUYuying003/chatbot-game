import pyaudio

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                output=True,
                frames_per_buffer=1024)

print("🎧 Loopback running... say something! (Ctrl+C 停止)")
try:
    while True:
        data = stream.read(1024, exception_on_overflow=False)
        stream.write(data)
except KeyboardInterrupt:
    pass
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Stopped.")