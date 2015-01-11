import pyaudio
import time
import wave
from struct import unpack
from threading import Thread

CHUNK_SIZE = 2 ** 10
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
UNPACK_FORMAT = '%ih' % (CHUNK_SIZE * CHANNELS)
MAX_VALUE = 32768

MIN_CLAP_GAP = .1
MAX_CLAP_GAP = 1
CLAP_THRESHOLD = .3


def wait_for_claps(num_claps, timeout=None):
    start = time.time()
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK_SIZE)

    while(True):
        clap_count = 0
        last_clap_time = 0

        while(True):
            now = time.time()
            if timeout and now - start > timeout:
                return
            if last_clap_time and now - last_clap_time > MAX_CLAP_GAP:
                break
            data = unpack(UNPACK_FORMAT, stream.read(CHUNK_SIZE))
            peak_amplitude = max(abs(float(x) / MAX_VALUE) for x in data)
            if peak_amplitude > CLAP_THRESHOLD and \
                    now - last_clap_time > MIN_CLAP_GAP:
                clap_count += 1
                print clap_count
                last_clap_time = now

        if clap_count == num_claps:
            return

    stream.stop_stream()
    stream.close()
    p.terminate()


class ClapListener(Thread):

    def __init__(self, *args, **kwargs):
        Thread.__init__(self, target=wait_for_claps, args=args, kwargs=kwargs)
        Thread.start(self)