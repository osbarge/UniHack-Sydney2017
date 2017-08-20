#for gui
import sys
from tkinter import *

#for speech
import speech_recognition as sr
from time import *
import time
import os
import pymysql

global question_num
question_num = 0
global q_list
q_list = ['what is your budget range','how many bedrooms you need?','start date','end date']
global inform
inform = {}
global current
current = ''
global attribute
attribute = list()


def raiseError():
    data = "say sorry, i cant understand could u make it clear?"
    os.system('say sorry, i cant understand could u make it clear?')
    readdQuestion(current)
    print("Google Speech Recognition could not understand audio")



def isValidBudget(data):
    result = data.split()
    print(result)
    if len(result) not in [1,2]:
        return False
    if len(result) == 1:
        return result[0].isdigit()
    if len(result) == 2:
        left = result[0]
        right = result[1]
        return left.isdigit() and right.isdigit()
    return True

def isValidBedrooms(data):
    result = data.split()
    print(result)
    if len(result) != 1:
        return False
    return result[0].isdigit()

def processQuery(attribute):
    db = pymysql.connect(host = 'localhost', port = 3306, user = 'root', passwd = '123456', db = 'mysql',charset = 'utf8')
    cur = db.cursor()
    prices = attribute.pop(0)
    num_of_bed = attribute.pop(0)[0]
    sql = ''
    num_rooms = 0
    if len(prices) == 1:
        price = prices[0]
        sql = "SELECT count(*) from hotel.rooms where price < "+price+" and num_of_bed = " + num_of_bed
    else:
        price1 = min(prices)
        price2 = max(prices)
        sql = "SELECT count(*) from hotel.rooms where price > "+price1+" and price < " + price2 +" and num_of_bed = " + num_of_bed
    try:
        cur.execute(sql)
        num_rooms = list(cur.fetchall())
        print(num_rooms)
        db.commit()
    except:
        print('fail')
        
    return (num_rooms[0][0] > 0)

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
                result = data.split()
                attribute.append(result)
            else:
                raiseError()
                
        if 'bedrooms' in current:
            if isValidBedrooms(data):
                inform['num_of_bed'] = data
                attribute.append(data.split())
            else:
                raiseError()
                

        data = "You said: " + data
        print(attribute)
        
        
        
    except sr.UnknownValueError:
        raiseError()
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
    q_list = ['What is your budget range?','How many bedrooms do you need?','start date','end date']
    print(q_list)
    global attribute
    global current
    attribute = list()
    current = popQuestion()
    

def readdQuestion(current):
    global q_list
    q_list = [current] + q_list


def popQuestion():
    if len(q_list) == 0:
        success = processQuery(attribute)
        if success == True:
            data = "say There is a room for you, your booking is reserved, thank you!"
            os.system(data)
        else:
            data = "say Sorry there is no such room available"
            os.system(data)
            
        return ''
        
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




