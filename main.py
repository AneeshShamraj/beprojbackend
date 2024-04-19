# IMPORT EXTERNAL PACKAGES
from fastapi import FastAPI, File, Form, UploadFile, Request, Response,Query,Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import smtplib
import imaplib
import ssl
from email.message import EmailMessage
import shutil
import email
# import yaml
import speech_recognition as sr
import os

from typing_extensions import Annotated
from typing import Union, List

from pydantic import BaseModel
#
class Recipients(BaseModel):
    recipients_address: List[str]




import moviepy.editor as moviepy
import json

# IMPORT FUNCTIONS FROM OTHER FILES
# from model import model_pipeline
# from audiofuncs import convert_audio
# from audiofuncs import audio

# INIT OBJECTS
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# with open("credentials.yml") as f:
#     content = f.read()
#
# # from credentials.yml import user name and password
# my_credentials = yaml.load(content, Loader=yaml.FullLoader)
#
# #Load the user name and passwd from yaml file
# user, password = my_credentials["user"], my_credentials["password"]
import os


import pydub


def process(string):
    string=string.lower()
    return string.replace(" ", "")


@app.get("/")
def read_root():
    return "Hello"



@app.post("/testaudio")
def test_audio(audio_data:UploadFile): #here audio is the key in the key value pair in frontend
    path1 = f"people/{audio_data.filename}"
    with open(path1, 'w+b') as file:
        shutil.copyfileobj(audio_data.file._file, file)
    return "Audio received successfully"

@app.post("/checkemail")
def check_email(user_email:str = Form()): #here audio is the key in the key value pair in frontend
    with open("data.json", "r") as f:
        data = json.load(f)

    # Filter the data based on a condition
    filtered_data = [obj for obj in data if obj["user"] == user_email]

    if len(filtered_data)==0:
        return {"isPresent":False}
    elif filtered_data[0]["path"]=="":
        return {"isPresent":False}
    else:
        return {"isPresent":True}

@app.post("/registerpassword")
def register_password(user_email:str = Form(),user_password:str = Form()): #here audio is the key in the key value pair in frontend
    with open("data.json", "r") as f:
        data = json.load(f)

    data.append({"user":user_email,"password":user_password,"path":""})
    with open("data.json", "w") as f:
        json.dump(data, f)
    return "Password received successfully"

@app.post("/registervoice")
def register_voice(audio_data:UploadFile,user_email:str = Form()): #here audio is the key in the key value pair in frontend
    path1 = f"people/{audio_data.filename}.wav"
    with open(path1, 'w+b') as file:
        shutil.copyfileobj(audio_data.file._file, file)

    with open("data.json", "r") as f:
        data = json.load(f)

    for account in data:
        if account["path"]=="" and account["user"]==user_email:
            account["path"]=path1

    with open("data.json", "w") as f:
        json.dump(data, f)

    return "Successful"


@app.post("/reademail")
async def read_email(user_email: str = Form()):
    # print(user)
    # user = "saneesh3152@gmail.com"
    password = "cgqi eyxd nycx xekf"
    print(password)
    #URL for IMAP connection
    imap_url = 'imap.gmail.com'

    # Connection with GMAIL using SSL
    my_mail = imaplib.IMAP4_SSL(imap_url)

    # Log in using your credentials
    my_mail.login(user_email, password)

    # Select the Inbox to fetch messages
    my_mail.select('Inbox')

    #Define Key and Value for email search
    #For other keys (criteria): https://gist.github.com/martinrusev/6121028#file-imap-search
    key = 'UNSEEN'
    _, data = my_mail.search(None, key)  #Search for emails with specific key and value

    mail_id_list = data[0].split()  #IDs of all emails that we want to fetch

    msgs = [] # empty list to capture all messages
    #Iterate through messages and extract data into the msgs list
    for num in mail_id_list:
        typ, data = my_mail.fetch(num, '(RFC822)') #RFC822 returns whole message (BODY fetches just body)
        msgs.append(data)

    #Now we have all messages, but with a lot of details
    #Let us extract the right text and print on the screen

    #In a multipart e-mail, email.message.Message.get_payload() returns a
    # list with one item for each part. The easiest way is to walk the message
    # and get the payload on each part:
    # https://stackoverflow.com/questions/1463074/how-can-i-get-an-email-messages-text-content-using-python

    # NOTE that a Message object consists of headers and payloads.
    resp=[]
    for msg in msgs[::-1]:
        mail={}
        for response_part in msg:
            if type(response_part) is tuple:
                my_msg=email.message_from_bytes((response_part[1]))
                mail['subject']=my_msg['subject']
                mail['from']=my_msg['from']
                body=""
                for part in my_msg.walk():
                    #print(part.get_content_type())
                    if part.get_content_type() == 'text/plain':
                        body=body+part.get_payload()
                mail['body']=body

        resp.append(mail)
    resp=resp[:5]
    json_compatible_item_data = jsonable_encoder(resp)
    return JSONResponse(content=json_compatible_item_data)
    # return str(resp)


@app.get("/readspecificemail")
def read_specific_email(user_email: str = Form(),sender_email: str = Form()):
    user="saneesh3152@gmail.com"
    password="cgqi eyxd nycx xekf"

    imap_url = 'imap.gmail.com'
    my_mail = imaplib.IMAP4_SSL(imap_url)
    my_mail.login(user, password)

    my_mail.select('Inbox')
    #For other keys (criteria): https://gist.github.com/martinrusev/6121028#file-imap-search
    _, data = my_mail.search(None, f'(HEADER FROM "{sender_email}")')  #Search for emails with specific key and value

    mail_id_list = data[0].split()  #IDs of all emails that we want to fetch

    msgs = [] # empty list to capture all messages
    #Iterate through messages and extract data into the msgs list
    for num in mail_id_list:
        typ, data = my_mail.fetch(num, '(RFC822)') #RFC822 returns whole message (BODY fetches just body)

        msgs.append({'data':data,'id':num})

    #Now we have all messages, but with a lot of details
    #Let us extract the right text and print on the screen

    #In a multipart e-mail, email.message.Message.get_payload() returns a
    # list with one item for each part. The easiest way is to walk the message
    # and get the payload on each part:
    # https://stackoverflow.com/questions/1463074/how-can-i-get-an-email-messages-text-content-using-python

    # NOTE that a Message object consists of headers and payloads.
    resp=[]
    for msg in msgs[::-1]:
        mail={}
        for response_part in msg:
            if type(response_part) is tuple:
                my_msg=email.message_from_bytes((response_part[1]))
                mail['subject']=my_msg['subject']
                mail['from']=my_msg['from']
                mail['id']=num
                body=""
                for part in my_msg.walk():
                    #print(part.get_content_type())
                    if part.get_content_type() == 'text/plain':
                        body=body+part.get_payload()
                mail['body']=body
        resp.append(mail)
    return resp




# @app.post("/voiceverification")
# def verify_user(audio_data:UploadFile):
#     # Define email sender and receiver
#     # email_sender = user
#     # email_password = password
#     # email_receiver = receiver
#     path1 = f"testaudiobucket/{audio_data.filename}.wav"
#     with open(path1, 'w+b') as file:
#         shutil.copyfileobj(audio_data.file._file, file)
#
#
#
#
#     bodyaudiofile=sr.AudioFile(path1)
#     bodytext=""
#     r = sr.Recognizer()
#     with bodyaudiofile as source:
#         audio = r.record(source)
#     try:
#         bodytext = r.recognize_google(audio)
#     except Exception as e:
#         print("Exception: "+str(e))
#     return {"body":bodytext,
#             "isVerified":True}

@app.post("/body")
def verification_with_body(audio_data:UploadFile,user_email: str = Form()):
    # Define email sender and receiver
    # email_sender = user
    # email_password = password
    # email_receiver = receiver
    #
    # print("For received audios:")
    # print(audio_data)
    # print(audio_data.file)
    # print(audio_data.file._file)
    # print(audio_data.filename)

    path1 = f"file.wav"
    with open(path1, 'w+b') as file:
        shutil.copyfileobj(audio_data.file._file, file)



    #
    # clip = moviepy.VideoFileClip("file.webm")
    # clip.audio.write_audiofile("out_audio.wav")
    # filename ="out_audio.wav"



    # Path


    # Join various path components

    # pathforwebmfile=os.path.join(os.getcwd(), "file.webm")
    # pathforwebmfile="C:/newvol/beprojfinal/beprojbackend/file.webm"
    # print(pathforwebmfile)

    # Path

    # Join various path components


    # # Join various path components
    # webm_file = pydub.AudioSegment.from_file(pathforwebmfile, format="webm")
    # print("After from file")
    # # Export the webm file as a wav file
    # webm_file.export("output.wav", format="wav")
    # print("After export")
    # filename="output.wav"


    r = sr.Recognizer()
    with sr.AudioFile(path1) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
    text=text.lower()
    # index=text.find('end body')
    # text=text[0:index]
    os.remove('file.wav')

    #PROCESS IT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    return {"body":text,
            "isVerified":True}



    # r = sr.Recognizer()
    #
    # hellow=sr.AudioFile(request.body)
    # with hellow as source:
    #     audio = r.record(source)
    # try:
    #     s = r.recognize_google(audio)
    #     print("Text: "+s)
    # except Exception as e:
    #     print("Exception: "+str(e))
    #
    # # Set the subject and body of the email
    # subject = emailsubject
    # body = emailbody
    #
    # em = EmailMessage()
    # em['From'] = email_sender
    # em['To'] = email_receiver
    # em['Subject'] = subject
    # em.set_content(body)
    #
    # # Add SSL (layer of security)
    # context = ssl.create_default_context()
    #
    # # Log in and send the email
    # with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    #     smtp.login(email_sender, email_password)
    #     smtp.sendmail(email_sender, email_receiver, em.as_string())
    #
    # return {"result":"Email sent"}
@app.post("/voiceverification")
def verify_user(audio_data:UploadFile,user_email: str = Form()):
    # Define email sender and receiver
    # email_sender = user
    # email_password = password
    # email_receiver = receiver

    # print("For received audios:")
    # print(audio_data)
    # print(audio_data.file)
    # print(audio_data.file._file)
    # print(audio_data.filename)
    #
    # path1 = f"{audio_data.filename}.wav"
    # with open(path1, 'w+b') as file:
    #     shutil.copyfileobj(audio_data.file._file, file)



    #
    # clip = moviepy.VideoFileClip("file.webm")
    # clip.audio.write_audiofile("out_audio.wav")
    # filename ="out_audio.wav"



    # Path


    # Join various path components

    # pathforwebmfile=os.path.join(os.getcwd(), "file.webm")
    # pathforwebmfile="C:/newvol/beprojfinal/beprojbackend/file.webm"
    # print(pathforwebmfile)

    # Path

    # Join various path components


    # # Join various path components
    # webm_file = pydub.AudioSegment.from_file(pathforwebmfile, format="webm")
    # print("After from file")
    # # Export the webm file as a wav file
    # webm_file.export("output.wav", format="wav")
    # print("After export")
    # filename="output.wav"


    # r = sr.Recognizer()
    # with sr.AudioFile(path1) as source:
    #     # listen for the data (load audio to memory)
    #     audio_data = r.record(source)
    #     # recognize (convert from speech to text)
    #     text = r.recognize_google(audio_data)
    # with open("data.json", "r") as f:
    #     data = json.load(f)

    # Filter the data based on a condition
    # filtered_data = [obj for obj in data if obj["user"] == user_email]


    # path1 = f"file.wav"
    # with open(path1, 'w+b') as file:
    #     shutil.copyfileobj(audio_data.file._file, file)
    #
    # result=model_pipeline(path1,filtered_data[0]["path"])
    # os.remove('file.wav')
    # return result
    return {"isVerified":True}

# @app.post("/compare")
# def compare_item(file1:UploadFile,file2:UploadFile):
#     print(file1)
#     print(file1.file)
#     print(file1.file._file)
#     print('testss')
#
#
#     result=model_pipeline(file1,file2)
#     return result

# @app.post("/read")
# def read_item(file1:UploadFile,file2:UploadFile):
#     verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")

#     # print(file1)
#     # print(file1.file)
#     # print(file1.file._file)
#     print('testss')

#     path1 = f"testset/{file1.filename}"
#     path2 = f"testset/{file2.filename}"

#     with open(path1, 'w+b') as file:
#         shutil.copyfileobj(file1.file, file)
#     with open(path2, 'w+b') as file:
#         shutil.copyfileobj(file2.file, file)

#     # file_path = f"testset/{file1.filename}"
#     # with open(file_path, "wb") as f:
#     #     f.write(file1.file.read())
#     score, prediction = verification.verify_files(path1,path2)
#     print(score)
#     print(prediction)


#     return {"prediction": prediction.item(),"score": score.item()}
    # result=model_pipeline(path1,path2)
    # return result


# @app.post("/read")
# def read_item(file1:UploadFile,file2:UploadFile):
#     # print(file1)
#     # print(file1.file)
#     # print(file1.file._file)
#     print('testss')
#
#     # path1 = f"testset/{file1.filename}"
#     # path2 = f"testset/{file2.filename}"
#
#     # with open(path1, 'w+b') as file:
#     #     shutil.copyfileobj(file1.file._file, file)
#     # with open(path2, 'w+b') as file:
#     #     shutil.copyfileobj(file2.file._file, file)
#
#     file_path = f"testset/{file1.filename}"
#     with open(file_path, "wb") as f:
#         f.write(file1.file.read())
#
#     # result=model_pipeline(path1,path2)
#     # return result

@app.post("/sendemail")
def send_email(user_email: str = Form(),og_sender: str = Form(),recipients_address: str = Form(...),subject: str = Form(),body: str = Form()):


    #CHANGE THIS IN FINAL CODE AND MAP USER
    user_email="saneesh3152@gmail.com"
    with open("data.json", "r") as f:
        data = json.load(f)

    # Filter the data based on a condition
    filtered_data = [obj for obj in data if obj["user"] == user_email]


    email_password=filtered_data[0]["password"]
    print(recipients_address)

    rec_list = json.loads(recipients_address)
    rec_list=list(map(process, rec_list))
    print(rec_list)

    em = EmailMessage()
    em['From'] = user_email
    em['To'] = ", ".join(rec_list)
    print(em['To'])
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(user_email, email_password)
        smtp.sendmail(user_email, rec_list, em.as_string())

    return {"sent":True}
