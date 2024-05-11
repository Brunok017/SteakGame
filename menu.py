import tkinter as tk
from tkinter import *
import subprocess
import sys
import os


window = tk.Tk()
window.title("High Steaks Menu")
window.geometry("600x600")

bg = PhotoImage(file=".\imgs\Background.png")

def play():
    window.destroy()
    subprocess.run(['python', 'main.py'])

def Settings():
    pass

def Quit():
    os.system('cls')
    sys.exit()


my_background = Label(window, image=bg)
my_background.place(x=0, y=0, relwidth=1, relheight=1)
label = tk.Label(window, text="High Steaks", font=("Arial", 24))
label.pack()
button = tk.Button(window, text="Play", command=play, font=("Arial", 20))
button.place(x=250, y=175)
button2 = tk.Button(window, text="Settings", command=Settings, font=("Arial", 20))
button2.place(x=230, y=275)
button3 = tk.Button(window, text="Quit", command=Quit, font=("Arial", 20))
button3.place(x=250, y=375)
window.mainloop()