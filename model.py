import torchaudio
# import speechbrain as sb
# from speechbrain.dataio.dataio import read_audio
# from IPython.display import Audio
from speechbrain.pretrained import SpeakerRecognition
# from speechbrain.pretrained import SepformerSeparation as separator


verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")





def model_pipeline(path1,path2):
    # signal, fs = torchaudio.load(file1.file)
    # signal2, fs = torchaudio.load(file2.file)
    # print(signal)
    # print(signal2)
    # score, prediction = verification.verify_batch(signal, signal2)
    score, prediction = verification.verify_files(path1,path2)


    return {"prediction": prediction,"score": score}
