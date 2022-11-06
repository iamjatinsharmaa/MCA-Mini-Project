import pyttsx3 as p
import pyjokes
import speech_recognition as sr
import datetime
from selenium import webdriver
import requests
import random
import randfacts
import time
import os
import webbrowser
import pywhatkit
from bs4 import BeautifulSoup

# search information on  wikipedia


class infow():
    def __init__(self):
        self.driver = webdriver.Chrome("C:\driver\chromedriver.exe")

    def get_info(self, query):
        self.query = query
        self.driver.get(url="https://www.wikipedia.org/")
        search = self.driver.find_element("xpath",
            '//*[@id="searchInput"]')
        search.click()
        search.send_keys(query)
        enter = self.driver.find_element("xpath",
            '//*[@id="search-form"]/fieldset/button')
        enter.click()

    # music play


class music():
    def __init__(self):
        self.driver = webdriver.Chrome("C:\driver\chromedriver.exe")

    def play(self, query):
        self.query = query
        self.driver.get(
            url="https://www.youtube.com/results?search_query=" + query)
        video = self.driver.find_element("xpath",
            '//*[@id="video-title"]/yt-formatted-string')
        video.click()
        time.sleep(50)

    # news api
api_address = "https://newsapi.org/v2/top-headlines?country=in&apiKey=e1c3737439c64c0293747f6edaaac43e"

json_data = requests.get(api_address).json()
today_news = []


def news():
    for i in range(3):
        today_news.append("Number "+str(i+1) + ", " +
                          json_data["articles"][i]["title"]+".")
    return today_news


def speak(text):
    engine = p.init()
    voices = engine.getProperty('voices')
    # use voices[0] for male voice
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 125)
    engine.say(text)
    engine.runAndWait()


def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning " + "Jatin how may I help you..")
        print(("Good Morning " + "Jatin how may I help you.."))
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon " + "Jatin how may I help you..")
        print("Good Afternoon " + "Jatin how may I help you..")
    else:
        speak("Good Evening " + "Jatin how may I help you..")
        print("Good Evening " + "Jatin how may I help you..")

def listenCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source, 1.2)
        text = ''
        speak("Listening...")
        # print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(text)
        except Exception as e:
            print(e)
            print("Say that again sir")
            return "None"
    return text

def questions():
    command = listenCommand()
    command = str(command).lower()

    if "what is your name" in command:
        speak('My name is groot ,How may i help you')
        print('My name is groot ,How may i help you')

    elif "wikipedia" in command:
        speak("you need information on what topic")
        inform = listenCommand()
        speak("Kindly wait i am searching for {} in wikipedia".format(inform))
        print("Kindly wait i am searching for {} in wikipedia".format(inform))
        webresult = infow()
        webresult.get_info(inform)
        speak("Information is  on the screen")
        print("Information is  on the screen")

    elif "song" in command:
        speak("  Which song would u like me to play")
        print("Which song would u like me to play")
        vid = str(listenCommand())
        speak("playing "+vid)
        assit = music()
        assit.play(vid)

    elif "news" in command:
        speak("sure sir, now i will read news for you")
        print("sure sir, now i will read news for you")
        top = news()
        for i in range(len(top)):
            print(top[i])
            speak(top[i])

    elif "jokes" in command:
        fun_jock = pyjokes.get_joke()
        speak("Ready for a laugh")
        print(fun_jock)
        speak(fun_jock)

    elif "fact" in command:
        speak("its fact time")
        print("its fact time")
        x = randfacts.getFact()
        print(x)
        speak("Did you know that ,"+x)

    elif "location" in command:
        speak('what is the location you want to search')
        print('what is the location you want to search')
        location = listenCommand()
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        speak('here is the location ' + location)

    elif "google" in command:
        speak("what would you like to search")
        search_ = listenCommand()
        url = 'https://google.com/search?q=' + search_
        webbrowser.get().open(url)
        print("your informtaion is displayed")
        speak("your informtaion is displayed")

    elif "time" in command:
        time_now = time.ctime()
        print(time_now)
        speak(time_now)

    elif "exit" in command:
        speak("By have a nice day")
        print("By have a nice day")
        exit()

    elif "whatsapp" in command:
        speak("what is your messege")
        print("what is your messege?")
        messege_ = listenCommand()
            # print(messege_)
        speak("whom you want to send messege")
        print("whom you want to send messege ?")
        no = {"My no.": '+918851551359',
                "Jio": '+919999999999', "Keshav": '+919990202651'}
        name = listenCommand()
        for name1, number in no.items():
            if name1 == name:
                 print(number)
        # print(number)
        # print(messege_)
        pywhatkit.sendwhatmsg_instantly(number,messege_)

    elif "temperature" in command:
        city = "temprature in Ghaziabad"
        url = f"https://www.google.com/search?q={city}"
        r = requests.get(url)
        data = BeautifulSoup(r.text, "html.parser")
        temp = data.find("div", class_="BNeawe").text
        speak(f"current   {city} is {temp}")
        print(f"current   {city} is {temp}")

    else:
        speak("sorry, can u say it again")

wishme()
while 1:
    command = questions()