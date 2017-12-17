Unpack software archive into some folder, e.g. C:\soundcard2txt

Go to https://www.anaconda.com/download/ and choose Python 3.6 version, 64-Bit Graphical Installer
or download directly: https://repo.continuum.io/archive/Anaconda3-5.0.1-Windows-x86_64.exe

Run anaconda prompt, change dir to C:\soundcard2txt [c:] [cd \soundcard2txt], then run: pip install -r requirements.txt

Detect the appropriate sound device, e.g., if we want to recognize audio from speakers, choose "Stereo Mix" device:
python recognize.py --list

Now we may run using chosen device and language, this will produce text recognition results file [recognition_log.txt]:
python recognize.py --device=3 --lang=ru-RU

Some unnecessary help available:
python recognize.py --help

List of supported languages and their codes: https://cloud.google.com/speech/docs/languages

Recognition quality can be improved using paid Google, Microsoft, IBM or other services.
