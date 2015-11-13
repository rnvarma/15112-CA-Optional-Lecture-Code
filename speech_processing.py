# Disclaimer: This code was written in about 2 h and is only meant to give you
# a general idea of how you would write a speech dialog system and how to 
# integrate an API with you project. The code is not very robust but the 
# general ideas should help you move forward. 

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from apiclient import errors
import oauth2client
from oauth2client import client
from oauth2client import tools

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import mimetypes
import base64

import speech_recognition as sr

import re

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://mail.google.com/'
# This is the file you would download from the Google API website once you
# set up the permission for you account. Follow the tutorial here: 
# https://developers.google.com/gmail/api/quickstart/python
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API TP presentation'


"""
Gets valid user credentials from storage.

If nothing has been stored, or if the stored credentials are invalid,
the OAuth2 flow is completed to obtain the new credentials.

Returns:
    Credentials, the obtained credential.
"""
def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-tp-presentation.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

"""
Create a message for an email.

Args:
sender: Email address of the sender.
to: Email address of the receiver.
subject: The subject of the email message.
message_text: The text of the email message.
file_dir: The directory containing the file to be attached.
filename: The name of the file to be attached.

Returns:
An object containing a base64url encoded email object.

"""
def createMessageWithAttachment(
    sender, to, subject, message_text, file_dir, filename):

    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    path = os.path.join(file_dir, filename)
    content_type, encoding = mimetypes.guess_type(path)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(path, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(path, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(path, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(path, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()

    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    return {'raw': base64.urlsafe_b64encode(message.as_string())}


"""
Create a message for an email.

Args:
sender: Email address of the sender.
to: Email address of the receiver.
subject: The subject of the email message.
message_text: The text of the email message.

Returns:
An object containing a base64url encoded email object.
"""
def createMessage(sender, to, subject, message_text):

    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string())}

def sendMessage(service, sender, to, subject, message_text):
    message = createMessage(sender, to, subject, message_text)
    try:
        result = (service.users().messages().send(userId="me", body=message)
                .execute())
        print("Message sent successfully")
    except errors.HttpError, error:
        print("An error occurred %s", error)


class State(object):
    def __init__(self, name, introSpeech=""):
        self.name = name
        self.intoSpeech = introSpeech

    def getName(self):
        return self.name

    def execute(self, recognizer, speak=True):
        if (self.intoSpeech != "" and speak):
            os.system("say %s" % self.intoSpeech)
        while (True):
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
            try:
                s = recognizer.recognize_google(audio)
                return s
            except:                       
                os.system("say %s" % "I'm sorry I did not get that. Could you repeat?")

class FSM(object):
    def __init__(self, states, transitions, service):
        self.states = states
        self.transitions = transitions
        self.recognizer = sr.Recognizer()
        self.curState = states[0]
        self.service = service

    def transition(self, input):
       nextState = self.transitions[self.curState.name].get(input, None)
       if (nextState == None): return
       else: self.curState = [state for state in self.states if state.name == nextState][0]

    def parseEmail(self, response):
        match = re.search('(\w+)\s(\w+)\s(to\s)(\w+)(\s*\d*\s*)(\sat\s)(\w+\.\w+)',
                response)
        if match:
            if (match.group(1) == "send" or match.groups(1) == "compose"):                      
                return "%s@%s" % (match.group(4), match.group(6)) 
        return None

    def parseMessage(self, response):
        parsedResponse = ""
        words = response.split(" ")
        i = 0
        while (i < len(words)):
            word = words[i]
            if (i < len(words) - 1 and word == "new" and words[i + 1] == "line"):
                parsedResponse += "\n"
                i += 2
            elif word == "period":
                parsedResponse += "."
                i += 1
            elif word == "comma":
                parsedResponse += "."
                i += 1
            else:
                parsedResponse += word
                i += 1
            parsedResponse += " "
        return parsedResponse

    def start(self):
        # start the FSM in the init stage
        userInput = self.curState.execute(self.recognizer)
        while (self.parseEmail(userInput) == None):
            # try to get a valid email address
            userInput = self.curState.execute(self.recognizer)
        email = userInput # we finally got a valid email address 
        self.transition("send")
        userInput = self.curState.execute(self.recognizer)
        curMessage = self.parseMessage(userInput)
        message = ""
        while ("send" not in curMessage.lower()):
            message += curMessage
            userInput = self.curState.execute(self.recognizer, False)
            curMessage = self.parseMessage(userInput)
        sendMessage(self.service, "rmorina@andrew.cmu.edu", email, "YAY", 
            message)
        
def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    init = State("init", "starting")
    composing = State("composing", "Okay, ready to compose email")
    attachment = State("attachment")

    states = [init, composing, attachment]
    transitions = {
                    "init": {"send": "composing", "compose": "composing"},
                    "composing": {"send": "init"},
                   }

    FSM_112 = FSM(states, transitions, service)
    FSM_112.start()



if __name__ == '__main__':
    main()