from speechbrain.pretrained import SpeakerRecognition



verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")





def model_pipeline(path1,path2):

    score, prediction = verification.verify_files(path1,path2)


    return {"prediction": prediction,"score": score}
