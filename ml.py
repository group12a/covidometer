import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
import pyttsx3
import speech_recognition as sr
class ml:
    def ab(self):
        data = pd.read_csv(r'https://raw.githubusercontent.com/group12a/covidometer/main/world.csv')
        data = data[['days','world']]
        print('_'*40);print('\t\tHead');print('_'*40)
        print(data.head())
        print('-'*40);print('prepare data');print('-'*40)
        x = np.array(data[f'days']).reshape(-1,1)
        y = np.array(data[f'world']).reshape(-1,1)
        plt.plot(y,'-c')
        plt.xlabel("Number of days")
        plt.ylabel("World cases in Millions")

        polyfeat = PolynomialFeatures(degree = 2)
        x = polyfeat.fit_transform(x)
        # print(x)

        print('_'*40);print('\t\tTraining data');print('_'*40)
        model = linear_model.LinearRegression()
        model.fit(x,y)
        accuracy = model.score(x,y)
        print(f'Accuracy:{round(accuracy*100,3)} %')
        y0 = model.predict(x)
        # plt.plot(y0,'--m')
        # plt.show()

        speak("\n Enter the number of days you want this to predict: ")
        n = int(input('\n Enter the number of days you want this to predict: '))
        print(f'prediction - cases after {n} days: ',end='')
        num = round(int(model.predict(polyfeat.fit_transform([[522+n]])))/1000000,2)
        print(round(int(model.predict(polyfeat.fit_transform([[522+n]])))/1000000,2),'Million')
        speak(num)
        speak("million")
        x1 = np.array(list(range(434+n))).reshape(-1,1)
        y1 = model.predict(polyfeat.fit_transform(x1))
        plt.plot(y1,'--r')
        plt.plot(y0,'--y')
        plt.show() 

'''This function is used to speak'''
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    obj =  ml()
    obj.ab()
