#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 10:38:19 2019

@author: saurabh
"""
import tkinter as tk
import requests
from tkinter import *
from datetime import datetime
class Location:
    loc=""              #city
    country=""
    country_code=""
    region_name=""      #state
    ZIP=""              #pin code
    
    def __init__(self):
        loc_response=requests.get("http://ip-api.com/json/")
        loc_response=loc_response.json()
        Location.loc=loc_response['city']
        Location.country=loc_response['country']
        Location.country_code=loc_response['countryCode']
        Location.region_name=loc_response['regionName']
        Location.ZIP=loc_response['zip']
        
    def current_weather(self,loc):
        crr_wtr_response=requests.get("http://api.openweathermap.org/data/2.5/weather?q={}&appid=ceb5be095227088eeae0290ebe379a19".format(loc))
        crr_wtr_response=crr_wtr_response.json()
        self.crr_temp=(str(round(crr_wtr_response['main']['temp']-273.15))+"°")
        self.crr_description=crr_wtr_response['weather'][0]['description']
        self.crr_pressure=str(crr_wtr_response['main']['pressure'])+"hPa"
        self.crr_humidity=str(crr_wtr_response['main']['humidity'])+"%"
        self.crr_min_temp=(str(round(crr_wtr_response['main']['temp_min']-273.15))+"°")
        self.crr_max_temp=(str(round(crr_wtr_response['main']['temp_max']-273.15))+"°")
        self.crr_wind_deg=crr_wtr_response['wind']['deg']
        if self.crr_wind_deg>=348.75 and self.crr_wind_deg<=11.25:
            self.crr_wind_dir="N"
        elif self.crr_wind_deg>11.25 and self.crr_wind_deg<=33.77:
            self.crr_wind_dir="NNE"
        elif self.crr_wind_deg>33.75 and self.crr_wind_deg<=56.25:
            self.crr_wind_dir="NE"
        elif self.crr_wind_deg>56.25 and self.crr_wind_deg<=78.75:
            self.crr_wind_dir="ENE"
        elif self.crr_wind_deg>78.75 and self.crr_wind_deg<=101.25:
            self.crr_wind_dir="E"
        elif self.crr_wind_deg>101.25 and self.crr_wind_deg<=123.75:
            self.crr_wind_dir="ESE"
        elif self.crr_wind_deg>123.75 and self.crr_wind_deg<=146.25:
            self.crr_wind_dir="SE"
        elif self.crr_wind_deg>146.25 and self.crr_wind_deg<=168.75:
            self.crr_wind_dir="SSE"
        elif self.crr_wind_deg>168.75 and self.crr_wind_deg<=191.25:
            self.crr_wind_dir="S"
        elif self.crr_wind_deg>191.25 and self.crr_wind_deg<=213.75:
            self.crr_wind_dir="SSW"
        elif self.crr_wind_deg>213.75 and self.crr_wind_deg<=236.25:
            self.crr_wind_dir="SW"
        elif self.crr_wind_deg>236.25 and self.crr_wind_deg<=258.75:
            self.crr_wind_dir="WSW"
        elif self.crr_wind_deg>258.75 and self.crr_wind_deg<=281.25:
            self.crr_wind_dir="W"
        elif self.crr_wind_deg>281.25 and self.crr_wind_deg<=303.75:
            self.crr_wind_dir="WNW"
        elif self.crr_wind_deg>303.75 and self.crr_wind_deg<=326.25:
            self.crr_wind_dir="NW"
        elif self.crr_wind_deg>326.25 and self.crr_wind_deg<348.75:
            self.crr_wind_dir="NNW"
        self.crr_wind=str(self.crr_wind_dir)+" "+str(crr_wtr_response['wind']['speed'])+"km/h"
        self.sunrise=str(datetime.fromtimestamp(crr_wtr_response['sys']['sunrise']))[10:16]
        self.sunset=str(datetime.fromtimestamp(crr_wtr_response['sys']['sunset']))[10:16]
    def future_weather(self,loc):
        self.list_ftr=[]
        ftr_wtr_response=requests.get("http://api.openweathermap.org/data/2.5/forecast?q={}&mode=json&appid=ceb5be095227088eeae0290ebe379a19".format(loc))
        ftr_wtr_response=ftr_wtr_response.json()
        for i in  ftr_wtr_response['list']:
            time=i['dt_txt'][11:16]
            temperature=str(round(i['main']['temp']-273.15))+"°"
            description=i['weather'][0]['description']
            self.list_ftr.append(" "+str(time)+"   "+temperature+"  "+description.capitalize())
    
    def pollution(self,loc,region_name,country):
        pollution_response=requests.get("http://api.airvisual.com/v2/city?city={}&state={}&country={}&key=cc495117-df0d-4f8d-a47e-a406cefa26f9".format(loc,region_name,country))
        pollution_response=pollution_response.json()
        try:
            self.aqi=pollution_response['data']['current']['pollution']['aqius']
            major_pollutant=pollution_response['data']['current']['pollution']['mainus']
            if(major_pollutant=='p2'):
                self.main_pollutant="pm2.5"
            elif(major_pollutant=='p1'):
                self.main_pollutant="pm10"
            elif(major_pollutant=='o3'):
                self.main_pollutant="Ozone O3"
            elif(major_pollutant=='n2'):
                self.main_pollutant="Nitrogen dioxide NO2"
            elif(major_pollutant=='s2'):
                self.main_pollutant="Sulphur dioxide SO2"
            elif(major_pollutant=='co'):
                self.main_pollutant="Carbon monoxide CO"
            else:
                self.main_pollutant="Not Found"
        except:
            self.aqi='Not Found'
            self.main_pollutant='Not Found'
    def new_data(self,loc):
        new_data_response=requests.get("https://api.opencagedata.com/geocode/v1/json?q={}&key=a68be540b6984951bbe5e21594c84ac7".format(loc))
        new_data_response=new_data_response.json()
        Location.country=new_data_response['results'][0]['components']['country']
        Location.region_name=new_data_response['results'][0]['components']['state']
        
l=Location()
l.current_weather(l.loc)
l.future_weather(l.loc)
l.pollution(l.loc,l.region_name,l.country)
r = tk.Tk()
r.title("Weather") 
r.geometry("1400x800")
r.configure(bg='red4')

#code for current temperature
temp_now=Label(r)
temp_now.place(x=100,y=50)
temp_now.config(font=('times',100,'bold'),bg="red4", fg="snow")
def crr_temp(crr_temp):
    temp_now['text'] = crr_temp 

#codes for current location
loc_now=Label(r)
loc_now.place(x=900,y=80)
loc_now.config(font=('times',70,'bold'),bg="red4", fg="snow")
def crr_loc(loc):
    loc_now['text'] = loc
    
#codes for current description
cond_now=Label(r)
cond_now.config(font=('times',50,'bold'),bg="red4", fg="snow")
cond_now.place(x=50,y=180)
def crr_description(description):
    cond_now['text'] = description.capitalize()
    
#codes for pressure section
pressure=Label(r,text="Pressure")
pressure.config(font=('times',30,'bold'),bg="red4", fg="DodgerBlue3")
pressure.place(x=50,y=280)

pressure_now=Label(r)
pressure_now.config(font=('times',20,'bold'),bg="red4", fg="snow")
pressure_now.place(x=50,y=350)
def crr_pressure(pressure):
    pressure_now['text']=pressure

#codes for humidity section
humidity=Label(r,text="Humidity")
humidity.config(font=('times',30,'bold'),bg="red4", fg="DodgerBlue3")
humidity.place(x=250,y=280)

humidity_now=Label(r)
humidity_now.config(font=('times',20,'bold'),bg="red4", fg="snow")
humidity_now.place(x=300,y=350) 
def crr_humidity(humidity):
    humidity_now['text']=humidity
    
#codes for minimum temperature
min_temp=Label(r,text="Min.Temp")
min_temp.config(font=('times',30,'bold'),bg="red4", fg="DodgerBlue3")
min_temp.place(x=430,y=280)

min_temp_now=Label(r)
min_temp_now.config(font=('times',20,'bold'),bg="red4", fg="snow")
min_temp_now.place(x=470,y=350)
def crr_min_temp(min_temp):
    min_temp_now['text']=min_temp

#codes for maximum temperature
max_temp=Label(r,text="Max.Temp")
max_temp.config(font=('times',30,'bold'),bg="red4", fg="DodgerBlue3")
max_temp.place(x=620,y=280)

max_temp_now=Label(r)
max_temp_now.config(font=('times',20,'bold'),bg="red4", fg="snow")
max_temp_now.place(x=670,y=350) 
def crr_max_temp(max_temp):
    max_temp_now['text']=max_temp
    
#codes for wind speed
wind=Label(r,text="Wind")
wind.config(font=('times',30,'bold'),bg="red4", fg="DodgerBlue3")
wind.place(x=840,y=280)

wind_now=Label(r)
wind_now.config(font=('times',20,'bold'),bg="red4", fg="snow")
wind_now.place(x=800,y=350)
def crr_wind_speed(wind_speed):
    wind_now['text']=wind_speed

#codes for sunrise
sunrise=Label(r,text="Sunrise")
sunrise.config(font=('times',30,'bold'),bg="red4", fg="DodgerBlue3")
sunrise.place(x=1000,y=280)

sunrise_now=Label(r)
sunrise_now.config(font=('times',20,'bold'),bg="red4", fg="snow")
sunrise_now.place(x=1020,y=350)
def sunrise(sunrise_time):
    sunrise_now['text']=sunrise_time

#codes for sunset
sunset=Label(r,text="Sunset")
sunset.config(font=('times',30,'bold'),bg="red4", fg="DodgerBlue3")
sunset.place(x=1200,y=280)

sunset_now=Label(r)
sunset_now.config(font=('times',20,'bold'),bg="red4", fg="snow")
sunset_now.place(x=1210,y=350)
def sunset(sunset_time):
    sunset_now['text']=sunset_time


''' codes to set scrollbar for hourly weather report 
(we cannot add scrollbar ad set list to it, it will cause problem)'''

def hr_weather_report(hr_weather_list):
    hr_frame = Frame(r,background="red", highlightcolor="green", highlightthickness=1, width=480, height=315)  
    hr_frame.place(x=50,y=400) 
    hr_label=Label(hr_frame,text="Today's Weather",width=35) 
    hr_label.place(x=0,y=0)
    hr_label.config(font=('times',20,'bold'),bg="red4", fg="snow")
    hr_scrollbar=Scrollbar(hr_frame)
    hr_scrollbar.place(x=465,y=31)
    hr_list=Listbox(hr_frame,yscrollcommand=hr_scrollbar.set,width=33,height=23)
    hr_list.config(font=('times',20),bg='gray80')
    hr_list.place(x=0,y=31)
    hr_scrollbar.config( command = hr_list.yview )
    for line in hr_weather_list: 
        hr_list.insert(END, line) 

#codes to display pollution details
pollution=Label(r,text="Pollution")
pollution.config(font=('times',30,'bold'),bg="red4", fg="DodgerBlue3")
pollution.place(x=800,y=420)

#codes to display AQI
aqi=Label(r,text="Air Quality Index(AQI): ")
aqi.config(font=('times',20,'bold'),bg="red4", fg="snow")
aqi.place(x=700,y=500)

aqi_now=Label(r)
aqi_now.config(font=('times',20,'bold'),bg="red4", fg="snow")
aqi_now.place(x=1060,y=500)
def aqi(new_aqi):
    aqi_now['text']=new_aqi

#codes to display major pollutant
main_pollutant=Label(r,text="Main pollutant: ")
main_pollutant.config(font=('times',20,'bold'),bg="red4", fg="snow")
main_pollutant.place(x=700,y=550)

main_pollutant_now=Label(r)
main_pollutant_now.config(font=('times',20,'bold'),bg="red4", fg="snow")
main_pollutant_now.place(x=950,y=550)
def main_pollutant(new_main_pollutant):
    main_pollutant_now['text']=new_main_pollutant

#codes to take input from user to search for given city
city=Label(r,text="Enter City")
city.config(font=('times',20,'bold'),bg="red4", fg="snow")
city.place(x=400,y=20)

enter_city=Entry(r,width=20,font=('bold'))
enter_city.place(x=550,y=25)
def change_city():
    l.loc=enter_city.get().capitalize()
    crr_loc(l.loc)
    l.current_weather(l.loc)
    l.future_weather(l.loc)
    crr_temp(l.crr_temp)
    enter_city.delete(0, END)
    crr_description(l.crr_description)
    crr_pressure(l.crr_pressure)
    crr_humidity(l.crr_humidity)
    crr_min_temp(l.crr_min_temp)
    crr_max_temp(l.crr_max_temp)
    crr_wind_speed(l.crr_wind)
    sunrise(l.sunrise)
    sunset(l.sunset)
    hr_weather_report(l.list_ftr)
    l.new_data(l.loc)
    l.pollution(l.loc,l.region_name,l.country)
    aqi(l.aqi)
    main_pollutant(l.main_pollutant)
    
search_button=tk.Button(r,text='Search',command=change_city)
search_button.configure(font=('times',12,'bold'),bg='black',fg='snow')
search_button.place(x=765,y=21)


crr_temp(l.crr_temp) 


crr_loc(l.loc)

crr_description(l.crr_description)
 
crr_pressure(l.crr_pressure)

crr_humidity(l.crr_humidity)

crr_min_temp(l.crr_min_temp)

crr_max_temp(l.crr_max_temp)

crr_wind_speed(l.crr_wind)

sunrise(l.sunrise)

sunset(l.sunset)

hr_weather_report(l.list_ftr)

aqi(l.aqi)

main_pollutant(l.main_pollutant)
#codes to close the window
def close_window():
    r.destroy()

exit_button=tk.Button(text='EXIT',command=close_window)
exit_button.configure(font=('times',15,'bold'),bg='black',fg='snow')
exit_button.place(x=1200,y=650)

r.mainloop()

 
