import tkinter as tk
from tkinter import *
from tkinter import DISABLED
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from matplotlib.figure import Figure
import cv2
from PIL import Image, ImageTk

vid = cv2.VideoCapture(0)
width, height = 10, 180
vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
score_displayed = False

def open_camera():
    global score_displayed, label_widget, vid
    ret, frame = vid.read()
    face_cascade = cv2.CascadeClassifier('frontal.xml')

    # load the pre-trained eye detection model
    eye_cascade = cv2.CascadeClassifier('eye.xml')
    if score_displayed or not vid.isOpened() or not ret:
        return
    else:
        # convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)

            # loop through each eye and determine if it is looking towards the right top corner of the vision
            for (ex, ey, ew, eh) in eyes:
                eye_center = (x + ex + ew // 2, y + ey + eh // 2)
                cv2.circle(frame, eye_center, 2, (0, 255, 0), 2)
            
                # check if the eye is looking towards the right top corner of the vision
                if eye_center[0] > w//2 and eye_center[1] < h//2:
                    cv2.putText(frame,"lying", (20,100),fontFace=6,fontScale=1.0,color=(0,0,255),thickness=2)
        # Convert image from one color space to other
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
       
        # Capture the latest frame and transform to image
        captured_image = Image.fromarray(opencv_image)

        # Convert captured image to photoimage
        photo_image = ImageTk.PhotoImage(image=captured_image)
        # loop through each face and detect the eyes
        

        # Displaying photoimage in the label
        label_widget.photo_image = photo_image

        # Configure image in the label
        label_widget.configure(image=photo_image)

        # Repeat the same process after every 10 seconds
        label_widget.after(10, open_camera)


base = Tk()
dataset = pd.read_csv("pred.csv")
base.bind('<Escape>', lambda e: base.quit())

# Create a label and display it on app
label_widget = Label(base)
label_widget.pack(side=RIGHT, padx=10)
open_camera()

base.geometry('850x750')
base.title("Personality Form")
base.configure(bg='#6699CC')
base.attributes("-alpha", 0.9)  # set transparency


new_window=Toplevel()
new_window.geometry("500x500")
new_window.title("Graphs")
new_window.resizable(False,False)
new_window.attributes("-alpha",0.9)
new_window.geometry("800x560")




labl_0 = Label(base, text="Personality test", width=20, font=("bold", 20), bg='#6699CC', fg='black')
labl_0.place(x=200, y=53)


question_num = 0
selected_option = tk.IntVar()

q = dataset["Questions"]
intro = dataset["intro"]
think = dataset["think"]
intuition = dataset["intuition"]
judging = dataset["judging"]

#Question = dataset["question"]
Options = [0,1,2,3,4,5,6]
graphs=["intro/extro","thinking/feeling","intuition/observant","judging/perspective"]

int_score = 0
int_count = 0
t_score = 0
t_count = 0
intu_score = 0
intu_count = 0
j_score = 0
j_count = 0


def show_question():
    global question_num,selected_option,int_score,int_count,t_score,t_count,intu_score,intu_count,j_score,j_count
    question = q[question_num]
    question_label.configure(text=question, bg='#6699CC', fg='black')
    for i in range(7):
        option_label[i].configure(text=Options[i], bg='#6699CC', fg='black')
    #selected_option.set(0)
    question_num += 1

    for i in range(len(q)):
            print(q[i])
            choice = selected_option.get()
            print("Selected Choice:", choice)
            if choice >= 0 and choice <= 6:
                if intro[i] == 1:
                            int_score += choice
                            int_count += 6
                if think[i] == 1:
                            t_score += choice
                            t_count += 6
                if intuition[i] == 1:
                            intu_score += choice
                            intu_count += 6
                if judging[i] == 1:
                            j_score += choice
                            j_count += 6
    

def update_score():
    global selected_option
    personality = []


    if question_num == len(q):
        if int_score <= int_count / 2:
            personality.append("I")
        else:
            personality.append("E")
        if t_score <= t_count / 2:
            personality.append("T")
        else:
            personality.append("F")
        if intu_score <= intu_count / 2:
            personality.append("N")
        else:
            personality.append("O")
        if j_score <= j_count / 2:
            personality.append("J")
        else:
            personality.append("P")

        submit_button.configure(text='Personality type: ' + str(personality),
                                font=("bold", 10), width=45, height=6, bg='#000000', fg='white')
        submit_button.place(x=250, y=375)
        #score_displayed = True
        submit_button.configure(state=DISABLED)
    else:
        show_question()
    

question_label = Label(base, text='', width=80, font=("bold", 12), bg='#6699CC', fg='white')
question_label.place(x=13, y=120)
option_label = []
graph_label = []

for i in range(7):
    option = Radiobutton(base, text='', variable=selected_option, value=Options[i], font=("bold", 11), bg='black',
                         fg='black')
    option.place(x=75, y=200 + i * 30)
    option_label.append(option)

submit_button = Button(base, text='Next', width=20, bg='#023047', fg='white', command=update_score)
submit_button.place(x=285, y=380)
show_question()

def previous():
    #new_window.withdraw()
    base.withdraw()
    new_window.deiconify()

def previous2():
     new_window.withdraw()
     base.deiconify()


def graph(y):
     #z=np.array([x,y-x])
        if y==1:
            z=np.array([int_score,int_count-int_score])
            print(z)
            label=["introvert","extrovert"]
            myexplode=[0.3,0]
            plt.pie(z,labels=label,explode=myexplode)
            plt.show()
            plt.close()

        elif y==2:
            z=np.array([t_score,t_count-t_score])
            label=["think","feeling"]
            myexplode=[0.3,0]
            plt.pie(z,explode=myexplode,labels=label)
            plt.show()
            plt.close()
        elif y==3:
            z=np.array([intu_score,intu_count-intu_score])
            label=["intuition","observant"]
            myexplode=[0.3,0]
            plt.pie(z,explode=myexplode,labels=label)
            plt.show()
            plt.close()
        elif y==4:
            z=np.array([j_score,j_count-j_score])
            print(z)
            label=["judging","perceiving"]
            myexplode=[0.3,0]
            plt.pie(z,explode=myexplode,labels=label)
            plt.show()
            plt.close()
            

btn21=Button(base,text="View graph",command=previous,relief='sunken')
btn21.pack(side=BOTTOM, padx=10, pady=10)

btn22=Button(new_window,text="previous",command=previous2,relief='sunken')
btn22.pack(side=BOTTOM, padx=10, pady=10)

btn77=Button(new_window,text="graph",command=lambda:graph(1), font=("Arial", 25),relief='groove',activebackground="white")
btn77.place(x=55,y=140)
btn78=Button(new_window,text="graph",command=lambda:graph(2), font=("Arial", 25),relief='groove',activebackground="white")
btn78.place(x=85,y=140)
btn79=Button(new_window,text="graph",command=lambda:graph(3), font=("Arial", 25),relief='groove',activebackground="white")
btn79.place(x=115,y=140)
btn80=Button(new_window,text="graph",command=lambda:graph(4), font=("Arial", 25),relief='groove',activebackground="white")
btn80.place(x=155,y=140)


base.mainloop()