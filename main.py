import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read the data from a CSV file
dataset = pd.read_csv("pred.csv")
q = dataset["Questions"]
intro = dataset["intro"]
think = dataset["think"]
intuition = dataset["intuition"]
judging = dataset["judging"]

# Initialize variables to store scores and counts
int_score = 0
int_count = 0
t_score = 0
t_count = 0
intu_score = 0
intu_count = 0
j_score = 0
j_count = 0

def graph(y,label):
     #z=np.array([x,y-x])
     myexplode=[0.3,0]
     plt.pie(y,explode=myexplode,labels=label)
     plt.show()
     plt.close()

# Loop through the data and calculate scores and counts
for i in range(len(q)):
    print(q[i])
    choice = int(input("enter score from 0 to 6  : "))
    if choice>=0 and choice<=6:
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
    else:
        print("Invalid score")

# Calculate the MBTI personality type
personality = []
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

print(personality)
ar=int(input("Enter 1 for intro,2 for think,3 for intuition,4 for judge,5 for exit: "))
#lek=True
while(True):
    #ar=int(input("Enter 1 for intro,2 for think,3 for intuition,4 for judge: "))
    if ar==1:
        y=np.array([int_score,int_count-int_score])
        label=["introvert","extrovert"]
        print(y)
        graph(y,label)
    if ar==2:
        y=np.array([t_score,t_count-t_score])
        label=["think","feeling"]
        graph(y,label)
    if ar==3:
        y=np.array([intu_score,intu_count-intu_score])
        label=["intuition","observant"]
        graph(y,label)
    if ar==4:
        y=np.array([j_score,j_count-j_score])
        label=["judging","perceiving"]
        graph(y,label)
    elif ar==5:
        break
    
print(int_score)
print(int_count)
print(j_count)
print(j_score)
print(t_count)
print(t_score)
print(intu_count)
print(intu_score)

''' Calculate data and labels for each pie chart
intro_data = [("Introvert", int_score), ("Extrovert", int_count - int_score)]
think_data = [("Thinking", t_score), ("Feeling", t_count - t_score)]
intu_data = [("Intuition", intu_score), ("Sensing", intu_count - intu_score)]
j_data = [("Judging", j_score), ("Perceiving", j_count - j_score)]
'''

