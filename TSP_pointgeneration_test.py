: %matplotlib inline
import numpy as np
import math
import matplotlib.pyplot as plt
import copy
import random
import pandas
import csv
import time
from mpl_toolkits.basemap import Basemap

def distancelength(x1,y1,x2,y2):
    return np.linalg.norm(np.array([x1 - x2, y1 - y2]))

def NNplotupdate():
    ax.clear()
    ax.plot(finalX,finalY)
    ax.plot(allthexpoints,alltheypoints,'o')
    ax.set_title('Nearest Neighbor')
    ax.set_xlabel('X-Axis (meters)')
    ax.set_ylabel('Y-Axis (meters)')
    fig.canvas.draw()
    plt.pause(0.0000001)

def optplotupdate():
    ax.clear()
    ax.plot(twooptX,twooptY)
    ax.plot(finalX,finalY)
    ax.plot(allthexpoints,alltheypoints,'.')
    ax.set_title('2-opt')
    ax.set_xlabel('X-Axis (meters)')
    ax.set_ylabel('Y-Axis (meters)')
    fig.canvas.draw()
    plt.pause(0.0000001)

def pathlength(xpoints,ypoints):
    optdistance = 0
    for i in range(len(xpoints)-1):
        optdistance += distancelength(xpoints[i+1],ypoints[i+1],xpoints[i],ypoints[i])
    return optdistance
    

class Points:
    """ Points class represents x,y coords """
    def __init__(self, N):
        self.N = N
        
    def Xpoints(self):
        xpointz = []
        for i in range(N):
            xpointz.append(random.randint(-50,50))
        return xpointz
    def Ypoints(self):
        ypointz = []
        for i in range(N):
            ypointz.append(random.randint(-50,50))
        return ypointz
        


# Parameters
N = 10              # controls the number of points generated

"""
# Point generation
pointzzz = Points(N)
allthexpoints = pointzzz.Xpoints()
alltheypoints = pointzzz.Ypoints()
"""

allthexpoints = []
alltheypoints = []

with open('us-state-capitals.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]} \t {row[1]} \t {row[2]}\t{row[3]}')
            allthexpoints.append(float(row[2]))
            alltheypoints.append(float(row[3]))
            line_count += 1
    print(f'Processed {line_count} lines.')
    
# Configuring the plot
fig = plt.figure(figsize=(8, 8))
m = Basemap(projection='lcc', resolution=None,
            width=8E6, height=8E6,
            lat_0=45, lon_0=-100,)
m.etopo(scale=0.5, alpha=0.5)

# Map (long, lat) to (x, y) for plotting
x, y = m(-122.3, 47.6)
plt.plot(x, y, 'ok', markersize=5)
plt.text(x, y, ' Seattle', fontsize=12);


"""
ax = fig.add_subplot(111)
plt.ion()
fig.show()
fig.canvas.draw()

ax.clear()
ax.plot(allthexpoints,alltheypoints,'o')
"""
"""
# Nearest Neighbor
print("Starting the nearest neighbor algorithm...")
finalX = []
finalY = []
alltheXXpoints = copy.copy(allthexpoints)
alltheYYpoints = copy.copy(alltheypoints)
tempXval = 0
tempYval = 0
for i in range(len(allthexpoints)): #to cover all the points in the array
    distance = 1000000 #arbitrary long distance
    for j in range(len(alltheXXpoints)): #to cover all the unvisited points
        if distancelength(tempXval,tempYval,alltheXXpoints[j],alltheYYpoints[j]) < distance:
            distance = distancelength(tempXval,tempYval,alltheXXpoints[j],alltheYYpoints[j])
            indexsaver = j
    tempXval = alltheXXpoints[indexsaver]
    tempYval = alltheYYpoints[indexsaver]
    finalX.append(alltheXXpoints[indexsaver])
    finalY.append(alltheYYpoints[indexsaver])
    alltheXXpoints.pop(indexsaver)
    alltheYYpoints.pop(indexsaver)
    NNplotupdate()
finalX.append(finalX[0])
finalY.append(finalY[0])
NNplotupdate()
print("NN Produced a path length of {} meters".format(round(pathlength(finalX,finalY),2)))




############# 2-opt #############
twooptX = copy.copy(finalX)
twooptY = copy.copy(finalY)
oldX = 0
oldY = 0
shrinkingdistance = pathlength(twooptX,twooptY)
optswaplength = 3
print("Starting the 2-opt point swap...")
for i in range(len(twooptX)):
    for rand in reversed(range(0,5)):
        #rand = random.randint(1,3)
        oldX = twooptX[(i+(rand))%len(twooptX)]
        oldY = twooptY[(i+(rand))%len(twooptX)]
        twooptX[(i+(rand))%len(twooptX)] = twooptX[i]
        twooptY[(i+(rand))%len(twooptX)] = twooptY[i]
        twooptX[i] = oldX
        twooptY[i] = oldY
        optplotupdate()
        optdistance = pathlength(twooptX,twooptY)
        if optdistance < shrinkingdistance:     #keep the swap
            shrinkingdistance = optdistance
            optplotupdate()
            print(round(pathlength(twooptX,twooptY),2))
        else:                                   #undo the swap
            oldX = twooptX[(i+(rand))%len(twooptX)]
            oldY = twooptY[(i+(rand))%len(twooptX)]
            twooptX[(i+(rand))%len(twooptX)] = twooptX[i]
            twooptY[(i+(rand))%len(twooptX)] = twooptY[i]
            twooptX[i] = oldX
            twooptY[i] = oldY
            #optdistance = 0
initialdistance = round(pathlength(finalX,finalY) ,2)
print("Our initial distance was {} meters".format(initialdistance))
finaldistance = round(pathlength(twooptX,twooptY),2)
print("Our final distance is {} meters".format(finaldistance))
finalpercent = round(100*( (pathlength(finalX,finalY)/pathlength(twooptX,twooptY)) - 1),2)
print("Using 2-Opt point swapping, our final distance is {}% shorter".format(finalpercent))
# PLOTTING
ax.clear()
ax.plot(finalX,finalY)
ax.plot(allthexpoints,alltheypoints,'.')
ax.set_title('Optimized!')
ax.set_xlabel('X-Axis (meters)')
ax.set_ylabel('Y-Axis (meters)')
"""
