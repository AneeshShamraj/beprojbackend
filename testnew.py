import torchaudio
import speechbrain as sb
from speechbrain.dataio.dataio import read_audio
from IPython.display import Audio
from speechbrain.pretrained import SpeakerRecognition
from speechbrain.pretrained import SepformerSeparation as separator

# import required libraries
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

# Sampling frequency
# freq = 44100
freq=16000
# Recording duration
duration = 5

print('start')
# Start recorder with the given values
# of duration and sample frequency
recording = sd.rec(int(duration * freq),
                   samplerate=freq, channels=2)

# Record audio for the given number of seconds
sd.wait()
print('stop')

# This will convert the NumPy array to an audio
# file with the given sampling frequency
write("recording0.wav", freq, recording)
#
# # Convert the NumPy array to audio file
# wv.write("recording1.wav", recording, freq, sampwidth=2)

verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")



score, prediction = verification.verify_files(r"C:\Users\anees\Downloads\speakerident\recording0.wav", r"C:\Users\anees\Downloads\speakerident\people\bhoomi.wav") # Different Speakers
print(prediction, score)