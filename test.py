import torchaudio
import speechbrain as sb
from speechbrain.dataio.dataio import read_audio
from IPython.display import Audio
from speechbrain.pretrained import SpeakerRecognition
from speechbrain.pretrained import SepformerSeparation as separator


# verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")
#
#
#
# score, prediction = verification.verify_files(r"C:\Users\anees\Downloads\speakerident\people\aneesh.wav", r"C:\Users\anees\Downloads\speakerident\people\bhoomi.wav") # Different Speakers
# print(prediction, score)



# import os
# import wave
# print(os.listdir(r'C:\Users\anees\Downloads\speakerident\people'))
# for file_name in os.listdir(r'C:\Users\anees\Downloads\speakerident\people'):
#     with wave.open(file_name, "rb") as wave_file:
#         frame_rate = wave_file.getframerate()
#         print(frame_rate)


from scipy.io import wavfile
samplerate, data = wavfile.read('./testset/mihir.wav')
print(samplerate)
print(data)