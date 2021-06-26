import requests
import datetime
import json
import pyttsx3

'''This function is used to speak'''
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

speak('now this part shows us the vaccine availiabilty on today and for further four days')
speak('Enter the PIN code where you want the vaccine from')
POST_CODE = input("Enter PIN code: ") # 411014,600096,603103
speak('Enter the age you want to get vaccine for')
age = int(input('Enter the age: '))


# Print details flag
print_flag = 'Y'

speak('Enter the number of further days you want to check the availiability for')
numdays = int(input('Enter the number of further days you want to check the availiability for : '))


base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]


for INP_DATE in date_str:
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(POST_CODE, INP_DATE)
    response = requests.get(URL)
    if response.ok:
        resp_json = response.json()
        # print(json.dumps(resp_json, indent = 1))
        flag = False
        if resp_json["centers"]:
            speak('Available on')
            speak(format(INP_DATE))
            print("Available on: {}".format(INP_DATE))
            if(print_flag=='y' or print_flag=='Y'):
                for center in resp_json["centers"]:
                    for session in center["sessions"]:
                        if session["min_age_limit"] <= age:
                            print('-----------------------------------------------------------------------------------------------------------')
                            print("\t", center["name"])
                            print("\t", center["block_name"])
                            print("\t Price: ", center["fee_type"])
                            print("\t Available Capacity: ",  
                            session["available_capacity"])
                            speak('Available Capacity')
                            speak( session["available_capacity"])
                            if(session["vaccine"] != ''):
                                print("\t Vaccine: ", session["vaccine"])
                            print('--------------------------------------------------------------------------------------------------------------')
                            print('--------------------------------------------------------------------------------------------------------------')
                            print("\n")
                            
            
                
        else:
            speak('No available slots on ')
            speak(format(INP_DATE))
            print("No available slots on {}".format(INP_DATE))

