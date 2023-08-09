import nltk
from nltk.stem import WordNetLemmatizer
import speech_recognition as sr
from tkinter import *

# Program to make a simple
# login screen
import tkinter as tk
root = tk.Tk()
# setting the windows size
root.geometry("530x610")
root.resizable(height=FALSE,width=FALSE)
bg=PhotoImage(file='wallpaper.png')

canvas1 = Canvas(root,width=530,height=610)
canvas1.pack(fill='both',expand=FALSE)
canvas1.create_image(0,0,image=bg,anchor='nw')
# declaring string variable
# for storing name and password
name_var = tk.StringVar()

root.configure(bg='black')

# defining a function that will
# get the name and password and
# print them on the screen
def submit(self):
    global name
    name = name_var.get()
    print("The name is : " + name)

    name_var.set("")
    root.destroy()

def submit1():
    global name
    name = name_var.get()
    print("The name is : " + name)

    name_var.set("")
    root.destroy()
# creating a label for
# name using widget Label
name_label = tk.Label(root, text='Please Enter your name ',bg='black',foreground='white',font=('calibre', 17, 'bold'))

name_entry = tk.Entry(root, textvariable=name_var, font=('calibre', 17, 'bold'))

# Button that will call the submit function
sub_btn = tk.Button(root, text='Submit', command=submit)
root.bind('<Return>', submit)

sub_btn1 = tk.Button(root, text='Submit',bg='#83878a', command=submit1)

name_label.place(x=90,y=200,height=40,width=300)
name_entry.place(x=120,y=260,height=40,width=250)
sub_btn1.place(x=120,y=320,height=40,width=60)
# performing an infinite loop
# for the window to display
root.mainloop()

lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model

model = load_model('chatbot_model.h5')
import json
import random

intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - splitting words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stemming every word - reducing to base form
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for words that exist in sentence
def bag_of_words(sentence, words, show_details=True):
    # tokenizing patterns
    sentence_words = clean_up_sentence(sentence)
    # bag of words - vocabulary matrix

    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % word)
    return (np.array(bag))


def predict_class(sentence):
    # filter below  threshold predictions
    p = bag_of_words(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sorting strength probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if (i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result


# Creating tkinter GUI

#from tkinter import *



def send(self):
    msg = EntryBox.get().strip()
    # EntryBox.delete("0.0", END)

    if msg != '':

        ChatBox.config(state=NORMAL)
        ChatBox.insert(END, '\n'+name+": " + msg + '\n\n')

        ChatBox.config(foreground="white", font=("Cascadia Code", 12))

        ints = predict_class(msg)
        res = getResponse(ints, intents)

        ChatBox.insert(END, " 🤖=> " + res + '\n\n\n-------------------------------------------------------\n')

        ChatBox.config(state=DISABLED)
        ChatBox.yview(END)
    EntryBox.delete(0,END)

def send1():
    msg = EntryBox.get().strip()
    # EntryBox.delete("0.0", END)

    if msg != '':

        ChatBox.config(state=NORMAL)
        ChatBox.insert(END, '\n'+name+": " + msg + '\n\n')

        ChatBox.config(foreground="white", font=("Cascadia Code", 12))

        ints = predict_class(msg)
        res = getResponse(ints, intents)

        ChatBox.insert(END, " 🤖=> " + res + '\n\n\n-------------------------------------------------------\n')

        ChatBox.config(state=DISABLED)
        ChatBox.yview(END)
    EntryBox.delete(0,END)



def sptext():
    recognizer=sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print('recognizing...')
            data = recognizer.recognize_google(audio)
            print(data)
            EntryBox.insert(0,data)
        except sr.UnknownValueError:
            print('Not Understanding')


root = Tk()

root.configure(bg="#4a4c54")

root.title("  Chat-Bot")
root.geometry("530x610")
icon = PhotoImage(file='images.png')
root.iconphoto(True, icon)
root.resizable(width=FALSE, height=FALSE)


bg=PhotoImage(file='temp.png').subsample(1,1)
canvas2 = Canvas(root,width=530,height=610)
canvas2.pack(fill='both',expand=FALSE)
canvas2.create_image(0,0,image=bg,anchor='nw')
ChatBox = Text(root, bd=5 ,bg='black',height="8", width="50", font="Arial",wrap=WORD)

ChatBox.config(state=DISABLED)




# Bind scrollbar to Chat window
scrollbar = Scrollbar(root, command=ChatBox.yview, cursor="arrow")
ChatBox['yscrollcommand'] = scrollbar.set


photo = PhotoImage(file = "send.png")
photoimage = photo.subsample(5,5)

SendButton = Button(root, font=("Cascadia Code", 12, 'bold'), image=photoimage, bg="#c7c7c7", bd=0, compound=LEFT,command=send1)
root.bind('<Return>', send)

photo1 = PhotoImage(file='micro.png')
photoimage1=photo1.subsample(32,32)
VoiceButton = Button(root, font=("Cascadia Code", 12, 'bold'),image = photoimage1,bg="#4a4c54",bd=0,activebackground="black",compound = LEFT,command=sptext)


def clear_EntryBox():
    EntryBox.delete(0,END)
# Create the box to enter message
EntryBox = Entry(root, font=("Helvitica", 16))
EntryBox.pack()
scrollbar1 = Scrollbar(root,command=EntryBox.xview,orient=HORIZONTAL)
EntryBox['xscrollcommand'] = scrollbar1.set


ClearButton = Button(root,text="X",font=('Helvetica bold',10,'bold'),bg='black',foreground='white',compound=LEFT,command=clear_EntryBox)
# EntryBox = Text(root, bd=5, bg="white", width="29", height="5", font="Arial", fg='#000000')
# EntryBox.bind("<Return>", send)

# Place all components on the screen
scrollbar.place(x=512, y=6, height=480)
ChatBox.place(x=6, y=6, height=480, width=510)
EntryBox.place(x=123, y=513, height=60, width=340)
SendButton.place(x=13, y=510, height=62,width=70)
VoiceButton.place(x=470, y=523, height=38, width=38)
ClearButton.place(x=440,y=535,height=20,width=20)
scrollbar1.place(x=132,y=580,relheight=0.02,width=320)


# root.bind('<Return>',handler)

root.mainloop()