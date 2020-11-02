import requests
import json
import pyttsx3
import speech_recognition as sr
import re
import threading 
import time
import webbrowser

API_KEY = "tTo1zhTnu5rc"
PROJECT_TOKEN = "tCz7F-pioTor"
RUN_TOKEN = "t5rmjCOeeyRY"


class Data:
    '''this function takes api_key,projet_token and use it to fetch the data from the link specfied in get_data() function and init the program'''
    def __init__(self,api_key,project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key":self.api_key
        }
        self.data = self.get_data()
    '''loads data on real time from the specfied link below'''
    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data',params=self.params)
        data  =json.loads(response.text)
        return data
    '''fetches summation of all cases around the world'''   
    def get_total_cases(self):
        data = self.data['total']
        for content in data:
            if content['name'] == "Coronavirus Cases:":
                return content['value']
    '''fetches summation of death cases around the world'''
    def get_total_deaths(self):
        data = self.data['total']
        for content in data:
            if content['name'] == "Deaths:":
                return content['value']
        return "0"
    '''fetches summation of recovered cases around the world'''
    def get_total_recovered(self):
        data = self.data['total']
        for content in data:
            if content['name'] == "Recovered:":
                return content['value']
        return "0"
    '''This function get the country name and return the value of recovered,deceased and positive cases in those particular country only'''
    def get_country_data(self,country):
        data = self.data["country"]
        for content in data:
            if content['name'].lower() == country.lower():
                return content
        return "0"   
    '''This function get the list of all the countries'''
    def get_list_of_countries(self):
        countries = []
        for country in self.data['country']:
            countries.append(country['name'].lower())    
        return countries 
    ''' This Function is to fetch real time data from worldometer'''
    def update_data(self):
        response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run',params=self.params)
        
        def poll():
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.get_data()
                if new_data != old_data:
                    self.data = new_data
                    print("Data Updated")
                    speak("Data Updated")
                    # print(new_data)
                    break
                time.sleep(5)
        t  = threading.Thread(target=poll)
        t.start()
'''This function is used to speak'''
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
'''This function recognizes voices'''
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said=""
        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print("Exception:",str(e))
    return said.lower()

def main():
    print("Started Program")
    speak("How can I help you !")
    data = Data(API_KEY,PROJECT_TOKEN)
    country_list = data.get_list_of_countries()
    END_PHRASE = "stop"
    TOTAL_PATTERNS ={
        re.compile(r'[\w\s]' "+ total covid cases"): data.get_total_cases,
        re.compile(r'[\w\s]' "+ total "r'[\w\s]' "+ cases"): data.get_total_deaths,
        re.compile(r'[\w\s]' "+ total "r'[\w\s]' "+ deaths"): data.get_total_deaths,
        re.compile(r'[\w\s]' "+ total deaths"): data.get_total_deaths,
        re.compile(r'[\w\s]' "+ total "r'[\w\s]' "+ death"): data.get_total_deaths,
        re.compile(r'[\w\s]' "+ total death"): data.get_total_deaths,
        re.compile(r'[\w\s]' "+ total"r'[\w\s]' "+ recovered"): data.get_total_recovered,
        re.compile(r'[\w\s]' "+ total recovered cases"): data.get_total_recovered,
        re.compile(r'[\w\s]' "+ total recovered"): data.get_total_recovered,  
    }
    COUNTRY_PATTERNS ={
        re.compile(r'[\w\s]' "+ cases " r'[\w\s]'): lambda country: data.get_country_data(country)['total_cases'],
        re.compile(r'[\w\s]' "+ death " r'[\w\s]'): lambda country: data.get_country_data(country)['total_deaths'],
        re.compile(r'[\w\s]' "+ recovered " r'[\w\s]'): lambda country: data.get_country_data(country)['total_recovered'],
    }
    UPDATE_COMMAND = "update"
    while True:
        print("Listening...")
        text = get_audio()
        print(text)
        result = None

        for pattern, func in COUNTRY_PATTERNS.items():
            if pattern.match(text):
                words = set(text.split(" "))
                for country in country_list:
                    if country in words:
                        result = func(country)
                        break           

        for pattern, func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result = func()
                break
        if text == "who are you":
            result = "I am a Program created by IEM Students of group-12 for their minor project mentored by mr. ankan bhowmick"    

        if text == "who created you" or text == "who are your creators":  
            result = "I am created by IEM BCA students of 3rd year.My creators are neha , adrija , antara , progga , debarati"  

        if text == "open worldometer":
            result= "opening worldometer.It might take a moment"
            webbrowser.open("https://www.worldometers.info/coronavirus/")

        if text == "what is your role panda":
            result = "My role is to showcase the current schenario of covid 19 situation" 

        if text == UPDATE_COMMAND:
            result = "Data is being updated.This may take a moment!."
            data.update_data()
        if result:
            speak(result)
           
        if text.find(END_PHRASE) != -1: #stop program
            print('Exit')
            break


main()