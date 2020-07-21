import requests
import json
import PIL
from PIL import Image
from PIL import ImageTk
from tkinter import *

#get data from online api
web = requests.get("https://api.exchangeratesapi.io/latest")
#convert it to Currency Exchange format
data = web.json()
#add EUR rate as base
data["rates"]["EUR"] = 1

with open("exchange_rate.json", "w") as f:
    json.dump(data, f, indent = 2)

#make all the countries name into a list
country1 = []
for c in data["rates"]:
    country1.append(c)

country1.sort()
country2 = country1

win = Tk()
win.title("Currency exchanger")

#load the flag images
flag = {}
for c in data["rates"]:
    image = PIL.Image.open("images\\{}.png".format(c))
    image = image.resize((125,63))
    image = ImageTk.PhotoImage(image)
    flag[c] = image

exchangeIcon = PhotoImage(file = "images\\exchange.png")

Label(win, text = "Country").grid(row = 0, column = 0)
Label(win, text = "Country").grid(row = 0, column = 4)
Label(win, text="Last update : "+data["date"]).grid(row = 2)
Label(win, image=flag["AUD"]).grid(row=1, column=0, padx = 10)
Label(win, image=flag["AUD"]).grid(row=1, column=4, padx = 10)

def country1_option_click(country):
    Label(win, image=flag[country]).grid(row=1, column=0)

def country2_option_click(country):
    Label(win, image=flag[country]).grid(row=1, column=4)

#first country option menu
var_country1 = StringVar()
var_country1.set(country1[0])
country1_option = OptionMenu(win, var_country1, *country1, command = country1_option_click)
country1_option.grid(row = 1, column = 1)

#firs country entry box
country1_entry = Entry(win)
country1_entry.grid(row = 1, column = 2, padx = 10)

#second country option menu
var_country2 = StringVar()
var_country2.set(country2[0])
country2_option = OptionMenu(win, var_country2, *country2, command = country2_option_click)
country2_option.grid(row = 1, column = 5)

#second country entry box
country2_entry = Entry(win)
country2_entry.grid(row = 1, column = 6, padx = 10)

#calculation
def exchange():
    try:
        amount = float(country1_entry.get())
    except ValueError:
        Label(win, text = "Please input a number.", fg = "red").grid(row = 3, columnspan = 5)
        return
    country1_rate = data["rates"][var_country1.get()]
    country2_rate = data["rates"][var_country2.get()]
    country2_entry.delete(0, END)
    country2_entry.insert(0, (amount/country1_rate)*country2_rate)

Button(win, text = "Exchange", command = exchange, image = exchangeIcon, compound = LEFT).grid(row = 1, column = 3, padx = 10)

win.mainloop()
