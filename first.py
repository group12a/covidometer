import requests
import json
import pyttsx3
import speech_recognition as sr
import re
import threading
import time
import webbrowser
import os
import pyjokes

API_KEY = "tTo1zhTnu5rc"
PROJECT_TOKEN = "tAY0xDg7pqm0"
RUN_TOKEN =  "tUyP93sjzecd"


response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data',params={"api_key":API_KEY})

class Data:
    def __init__(self , api_key,project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key" : self.api_key
        }
        self.data = self.get_data()
    
    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data',params=self.params)
        data = json.loads(response.text)
        return data

    def get_total_cases(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Coronavirus Cases:":
                return content['value']

    def get_total_deaths(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Deaths:":
                return content['value']

    def get_total_recovered(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Recovered:":
                return content['value']
        
        return "0"

    def get_country_data(self,country):
        data = self.data["country"]

        for content in data:
            if content['name'].lower() == country.lower():
                return content
        
        return "0"

    def get_list_of_countries(self):
        countries = []
        for country in self.data['country']:
            countries.append(country['name'].lower())

        return countries

    def update_data(self):
        response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run',params=self.params)
        
        def poll():
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.get_data()
                if new_data != old_data:
                    self.data = new_data
                    print("Data updated")
                    speak("data updated")
                    break
                time.sleep(5)
                    
            


        t=threading.Thread(target=poll)
        t.start()

# print(data.get_country_data("india")['total_cases'])
# print(data.get_list_of_countries())

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print("Exception:",str(e))
        
    return said.lower()

def main():
    print("started Program")
    speak("started program welcome back madam")
    speak("How may I help you")
    data = Data(API_KEY,PROJECT_TOKEN)
    END_PHRASE = "stop"
    country_list = set(data.get_list_of_countries())

    TOTAL_PATTERNS ={
                    re.compile(r'[\w\s]' "+ total +"r'[\w\s]'"+ covid cases"):data.get_total_cases,
                    re.compile(r'[\w\s]' "+ worldwide +"r'[\w\s]'"+ cases"):data.get_total_cases,
					re.compile(r'[\w\s]' "+ total cases"): data.get_total_cases,
                    re.compile(r'[\w\s]'"+ total +"r'[\w\s]'"+ deaths"): data.get_total_deaths,
                    re.compile(r'[\w\s]'"+ worldwide +"r'[\w\s]'"+ deaths cases"): data.get_total_deaths,
                    re.compile(r'[\w\s]' "+ total death"): data.get_total_deaths,
                    re.compile(r'[\w\s]' "+ total recovered +"r'[\w\s]'"+ cases"):data.get_total_recovered,
                    re.compile(r'[\w\s]' "+ worldwide+"r'[\w\s]'"+ recovered cases"):data.get_total_recovered,
                    re.compile(r'[\w\s]' "+ recovered cases"):data.get_total_recovered,
                    }
    COUNTRY_PATTERNS = {
        re.compile(r'[\w\s]'"+ covid cases"r'[\w\s]'): lambda country: data.get_country_data(country)['total_cases'],
        re.compile(r'[\w\s]' "+ death cases"r'[\w\s]'): lambda country: data.get_country_data(country)['total_deaths'],
        re.compile(r'[\w\s]' "+ recovered cases"r'[\w\s]'): lambda country: data.get_country_data(country)['total_recovered'],
                        }
    UPDATE_COMMAND = "update"
    while True:
        print("Listening...")
        text = get_audio()
        print(text)
        result = None

        for pattern ,func in COUNTRY_PATTERNS.items():
            if pattern.match(text):
                words = set(text.split(" "))
                for country in country_list:
                    if country in words:
                        result = func(country)
                        break

        for pattern,func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result = func()
                break
            
        if text == UPDATE_COMMAND:
            result="Data is being updated this may take a moment"
            data.update_data()

        if text == "who are you":
            result = "I am a Program created by IEM Students of group-12 for their minor project mentored under mr. ankan bhowmick"
        
        if text == "open worldometer":
            webbrowser.open("https://www.worldometers.info/coronavirus/")
            result= "opening worldometer.It might take a moment"
        
        if text == "open world o metre":
            webbrowser.open("https://www.worldometers.info/coronavirus/")
            result= "opening worldometer.It might take a moment"
        
        if text == "open google":
            webbrowser.open("https://www.google.com/")
            speak("opening google. wait for a second")
        
        if text == "open github":
            webbrowser.open("https://github.com/group12a/covidometer")
            speak("opening github .wait for a second")
        
        if text == "what is your role":
            result = "My role is to showcase the current schenario of covid 19 pandemic in tracking with smart assistance" 

        # if text == "logout":
        #     result ="Logging out"
        #     os.system("shutdown -l")

        # if text == "shutdown":
        #     result ="shutting down"
        #     os.system("shutdown /s /t 1")

        # if text == "restart":
        #     result ="restarting"
        #     os.system("shut down /r /t 1")

        if text=="tell a joke":
            str=pyjokes.get_joke()
            # print(str)
            speak(str)
           
        if text=="quit":
            speak("Exitting as per your request")
            print('Exitting as per your request')
            break
        
        if text=="say hello":
            speak("Hello dear teachers . i  guess finally  todays  the  day  for  me  to  shine . I waited years for you to check me out")

        if result:
            speak(result)
            print(result)

        if text.find(END_PHRASE) != -1: #stop loop
            speak("Exitting as per your request")
            print('Exitting as per your request')
            break


main()