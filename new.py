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

labl_0 = Label(base, text="Personality test", width=20, font=("bold", 20), bg='#6699CC', fg='black')
labl_0.place(x=200, y=53)


question_num = 0
selected_option = IntVar()

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

def graph(y,score,count):
     #z=np.array([x,y-x])
        if y==1:
            z=np.array([score,count-score])
            print(z)
            label=["introvert","extrovert"]
            myexplode=[0.3,0]
            plt.pie(z,labels=label,explode=myexplode)
            plt.show()
            plt.close()

        elif y==2:
            z=np.array([score,count-score])
            label=["think","feeling"]
            myexplode=[0.3,0]
            plt.pie(z,explode=myexplode,labels=label)
            plt.show()
            plt.close()
        elif y==3:
            z=np.array([score,count-score])
            label=["intuition","observant"]
            myexplode=[0.3,0]
            plt.pie(z,explode=myexplode,labels=label)
            plt.show()
            plt.close()
        elif y==4:
            z=np.array([score,count-score])
            print(z)
            label=["judging","perceiving"]
            myexplode=[0.3,0]
            plt.pie(z,explode=myexplode,labels=label)
            plt.show()
            plt.close()


def show_question():
    global question_num,selected_option,int_score,int_count,t_score,t_count,intu_score,intu_count,j_score,j_count
    question = q[question_num]
    question_label.configure(text=question, bg='#6699CC', fg='black')
    for i in range(7):
        option_label[i].configure(text=Options[i], bg='#6699CC', fg='black')
    selected_option.set(0)
    question_num += 1

def update_score():
    global selected_option,int_score,int_count,t_score,t_count,intu_score,intu_count,j_score,j_count

    for i in range (len(q)):
        choice = selected_option.get()

        ar=[intro[i],think[i],intuition[i],judging[i]]
        for j,n in enumerate(ar):
             if j==0 and n==1:
                  int_score += choice
                  int_count += 6
             if j==1 and n==1:
                   t_score += choice
                   t_count += 6
             if j==2 and n==1:
                  intu_score += choice
                  intu_count += 6
             if j==3 and n==1:
                   j_score += choice
                   j_count += 6



    '''for i in range(len(q)):
        choice = selected_option.get()

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
                j_count += 6'''


    personality = []


    if question_num == len(q):
        print(int_score)
        print(int_count)
        print(j_count)
        print(j_score)
        print(t_count)
        print(t_score)
        print(intu_count)
        print(intu_score)
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
        '''for i in range(4):
            graph_label[i].configure(text=graphs[i], bg='#6699CC', fg='black')'''
        submit_button.place(x=250, y=375)
        #score_displayed = True
        submit_button.configure(state=DISABLED)
        btn77 = Button(base, text="Introvert ", command=lambda: graph(1, int_score, int_count), font=("Arial", 25), relief='groove', activebackground="white")
        btn77.place(x=55, y=140)
        btn78 = Button(base, text="Thinking", command=lambda: graph(2, t_score, t_count), font=("Arial", 25), relief='groove', activebackground="white")
        btn78.place(x=255, y=140)
        btn79 = Button(base, text="Intiution", command=lambda: graph(3, intu_score, intu_count), font=("Arial", 25), relief='groove', activebackground="white")
        btn79.place(x=455, y=140)
        btn80 = Button(base, text="Judgement", command=lambda: graph(4, j_score, j_count), font=("Arial", 25), relief='groove', activebackground="white")
        btn80.place(x=655, y=140)
        '''for i in range(4):
            graph_label[i].configure(text=graphs[i], bg='#6699CC', fg='black')
            opt = Button(base, text='', variable=selected_option,value=graphs[i], font=("bold", 11), bg='red',
                         fg='black',command=graph[i])
            opt.place(x=300, y=200 + i * 30)
            graph_label.append(opt)'''

    else:
         show_question()
#Question = dataset["question"]
#Options = [0,1,2,3,4,5,6]
'''root = tk.Tk()
frameChartsLT = tk.Frame(root)
frameChartsLT.pack()
y1=np.array([int_score,int_count-int_score])
label=["introvert","extrovert"]
explode1=[0.3,0]
#plt.pie(y1,labels=label,explode=explode1)
fig = Figure(figsize=(6, 4), dpi=100) # create a figure object
ax = fig.add_subplot(111) # add an Axes to the figure
ax.pie(y1, labels=label,explode=explode1)
chart1 = FigureCanvasTkAgg(fig,frameChartsLT)
chart1.get_tk_widget().pack()

root.mainloop()
#plt.show()'''


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
'''for i in range(4):
        #graph_label[i].configure(text=graphs[i], bg='#6699CC', fg='black')

        opt = Button(base, text='', value=Options[i], variable=selected_option,font=("bold", 11), bg='black',
                         fg='black')
        opt.place(x=300, y=200 + i * 30)
        graph_label.append(opt)'''


     





base.mainloop()