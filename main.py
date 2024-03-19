from typing import Union
from model import model_pipeline
from fastapi import FastAPI, UploadFile


import shutil

from speechbrain.pretrained import SpeakerRecognition
# verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")


app = FastAPI()

import smtplib
import ssl
from email.message import EmailMessage

import imaplib
import pprint

import email

import yaml

with open("credentials.yml") as f:
    content = f.read()

# from credentials.yml import user name and password
my_credentials = yaml.load(content, Loader=yaml.FullLoader)

#Load the user name and passwd from yaml file
user, password = my_credentials["user"], my_credentials["password"]


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/reademail")
def read_email():

    #URL for IMAP connection
    imap_url = 'imap.gmail.com'

    # Connection with GMAIL using SSL
    my_mail = imaplib.IMAP4_SSL(imap_url)

    # Log in using your credentials
    my_mail.login(user, password)

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

    for msg in msgs[::-1]:
        for response_part in msg:
            if type(response_part) is tuple:
                my_msg=email.message_from_bytes((response_part[1]))
                print("_________________________________________")
                print ("subj:", my_msg['subject'])
                print ("from:", my_msg['from'])
                print ("body:")
                for part in my_msg.walk():
                    #print(part.get_content_type())
                    if part.get_content_type() == 'text/plain':
                        print (part.get_payload())



@app.get("/sendemail")
def send_email():
    # Define email sender and receiver
    email_sender = user
    email_password = password
    email_receiver = 'umangumangspam@gmail.com'

    # Set the subject and body of the email
    subject = 'TEST1'
    body = """
    TEST1
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    return {"result":"Email sent"}

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

@app.post("/read")
def read_item(file1:UploadFile,file2:UploadFile):
    verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")

    # print(file1)
    # print(file1.file)
    # print(file1.file._file)
    print('testss')

    path1 = f"testset/{file1.filename}"
    path2 = f"testset/{file2.filename}"

    with open(path1, 'w+b') as file:
        shutil.copyfileobj(file1.file, file)
    with open(path2, 'w+b') as file:
        shutil.copyfileobj(file2.file, file)

    # file_path = f"testset/{file1.filename}"
    # with open(file_path, "wb") as f:
    #     f.write(file1.file.read())
    score, prediction = verification.verify_files(path1,path2)
    print(score)
    print(prediction)


    return {"prediction": prediction.item(),"score": score.item()}
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
