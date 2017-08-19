#for gui
import sys
from tkinter import *

#for speech
import speech_recognition as sr
from time import *
import time
import os

global question_num
question_num = 0
global q_list
q_list = ['what is your budget range','how many people are going with u?','start date','end date']
global inform
inform = {}
global current
current = ''


def isValidBudget(data):
    result = data.split()
    if len(result) not in [1,2]:
        return False
    if len(result) == 1:
        return type(result[0]) == int
    if len(result) == 2:
        left = result[0]
        right = result[1]
        return type(left) == int and type(right) == int


def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
 
    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        
        if 'budget' in current:
            if isValidBudget(data):
                inform['price'] = data
            else:
                data = "say sorry, i cant understand could u make it clear?"
                os.system('say sorry, i cant understand could u make it clear?')
                readdQuestion(current)
                print("Google Speech Recognition could not understand audio")
                
        if 'people' in current:
            inform['num_of_bed'] = data

        data = "You said: " + data
        print(inform)
        
        
    except sr.UnknownValueError:
        data = "say sorry, i cant understand could u make it clear?"
        os.system('say sorry, i cant understand could u make it clear?')
        readdQuestion(current)
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        data = "Could not request results from Google Speech Recognition service; "+e
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    
    return data

def getNecessaryQuestion():
    q = q_list.pop(0)
    return q
    
    
    
def reassign():
    print('reassign')
    global q_list
    q_list = ['what is your budget range','how many people are going with u?','start date','end date']
    print(q_list)

def readdQuestion(current):
    global q_list
    q_list = [current] + q_list
    
def popQuestion():
    if len(q_list) == 0:
        return None
    q = getNecessaryQuestion()

    print(q)
    os.system('say ' + q)
    print('lalalal')
    mlabel = Label(mGui,text = q).pack()
    return q 
    
def mhello():
    global current
##    mlabel = Label(mGui, text='Listening').pack()
##    tts = gTTS(text='Listening...', lang='en')
##    tts.save("audio.mp3")q
##    os.system("mpg321 audio.mp3")
    data = recordAudio()
    #while 1:
    mlabel = Label(mGui, text=data).pack()
    print("I'm done listening")

    current = popQuestion()
    print(current)
        
    
mGui = Tk()

mGui.geometry('450x450+500+300')
mGui.title('Eliza')

#mGui.mainlooop()
os.system('say welcome to book a room at hotel unihack!')
time.sleep(2)
mlabel = Label(mGui,text = 'say welcome to book a room at hotel unihack!').pack()
mlabel = Label(mGui, text='Press to speak').pack()
button = Button(mGui, text = 'Speak', command = mhello).pack()
button = Button(mGui, text = 'rebook', command = reassign).pack()
current = popQuestion()




