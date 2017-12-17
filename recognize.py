import argparse
import datetime
import pyaudio
import speech_recognition as sr
import threading
import time

recognizer = sr.Recognizer()
pa = pyaudio.PyAudio()

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--lang', type=str, default='en-US',
                    help='language to recognize, en-US, ru-RU, fi-FI or any other supported')
parser.add_argument('--buf', type=int, default=200,
                    help='buffer size to recognize')
parser.add_argument('--rate', type=int, default=48000,
                    help='audio sampling rate')
parser.add_argument('--device', type=int, default=0,
                    help='input device number')
parser.add_argument('--list', action='store_true', help='list audio devices and their numbers')
args = parser.parse_args()
if args.list:
    for i in range(0, pa.get_device_count()):
        print(i, " - ", pa.get_device_info_by_index(i)['name'])
    exit()

audio_rate = args.rate
stream_buf = bytes()
stream_counter = 0


def recognize(stream_text):
    global args

    def logger(s):
        f = open('recognition_log.txt', 'a+', encoding='utf-8')
        f.write(datetime.datetime.now().strftime("[ %d-%b-%Y %H:%M:%S ] "))
        f.write(s)
        f.write("\x0A")
        f.close()

    audio_data = sr.AudioData(stream_text, audio_rate, 2)
    try:
        # result = recognizer.recognize_sphinx(audio_data)
        result = recognizer.recognize_google(audio_data, language=args.lang)
        print(result)
        logger(result)
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print("Could not request results from GSR service; {0}".format(e))


def stream_audio(data):
    global args
    global stream_buf
    global stream_counter

    if stream_counter < args.buf:
        stream_buf += data
        stream_counter += 1
    else:
        threading.Thread(target=recognize, args=(stream_buf,)).start()
        stream_buf = bytes()
        stream_counter = 0


def callback(in_data, frame_count, time_info, status):
    stream_audio(in_data)
    return (None, pyaudio.paContinue)


stream = pa.open(format=pyaudio.paInt16, channels=1, rate=audio_rate, input=True, stream_callback=callback,
                 input_device_index=args.device)
stream.start_stream()
while stream.is_active(): time.sleep(0.1)
stream.stop_stream()
stream.close()
pa.terminate()
