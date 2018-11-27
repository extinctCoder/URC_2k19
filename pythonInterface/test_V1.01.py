# Created by Hadi, Abir Mohammad | 2018

import math
import os
import subprocess
import time
import gpsd


# import serial

# conn0 = serial.Serial('/dev/ttyACM0')


def SendDat(x):
    conn0.write(x.encode('ascii'))


def calc_dist(l1, lo1, l2, lo2):
    rad = 6371

    lat1 = math.radians(l1)
    lon1 = math.radians(lo1)

    lat2 = math.radians(l2)
    lon2 = math.radians(lo2)

    del_lat = lat2 - lat1
    del_long = lon2 - lon1

    # Distance calculated through Haversine Formula [https://en.wikipedia.org/wiki/Haversine_formula]
    a = math.sin(del_lat / 2) ** 2 + (math.cos(lat1) * math.cos(lat2) * math.sin(del_long / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))

    dist = rad * c

    return dist  # Error margin 10%


# Intermediate point calculation with Predefined step size
def intPtr(s, l1, lo1, l2, lo2):
    dR = calc_dist(l1, lo1, l2, lo2) / 6371
    l1 = math.radians(l1)
    lo1 = math.radians(lo1)
    l2 = math.radians(l2)
    lo2 = math.radians(lo2)

    a = math.sin((1 - s) * dR) / math.sin(dR)
    b = math.sin(s * dR) / math.sin(dR)

    x = a * math.cos(l1) * math.cos(lo1) + b * math.cos(l2) * math.cos(lo2)
    y = a * math.cos(l1) * math.sin(lo1) + b * math.cos(l2) * math.sin(lo2)
    z = a * math.sin(l1) + b * math.sin(l2)

    lat = math.degrees(math.atan2(z, math.sqrt(x * x + y * y)))
    lon = math.degrees(math.atan2(y, x))

    arr = [lat, lon]

    return arr


def con():
    gpsd.connect(host="127.0.0.1", port=50000)


def cur():
    arr = [gpsd.get_current().lat, gpsd.get_current().lon]

    return arr


'''
def getData():
    dat = conn0.readline().decode('utf-8')
    dat = dat.strip('\n')
    dat = dat.strip('\r')
    return int(dat)

def Direction(l1, lo1, l2, lo2):

    return int(math.atan2((l2-l1)/(lo2-lo1)))'''

l2 = 38.37405  # float(input("Destination Latitude in Decimal Degrees: "))
lo2 = -110.70802  # float(input("Destination Longitude in Decimal Degrees: "))
con()
arr = cur()
t_dist = calc_dist(arr[0], arr[1], l2, lo2)

stepDist = 0.01
curStp = 0

# time.sleep(2)
print("Distance from A to B: ", t_dist, " Km\n")
print(arr)

'''print("Getting Heading\n")
angle = getData() #Direction(arr[0], arr[1], l2, lo2)
print("Recorded Heading:", angle, "\n")'''

while (calc_dist(arr[0], arr[1], l2, lo2) > 0.004):
    ''' if((angle-const+360)%360 < 180):
     #Move Counter Clockwise
 
         while(angle != const):
             SendDat('r')
             const = getData()
 
             print("Current: ", const, "\nDir: ", angle, "\n")
 
         SendDat('z')
 
     else:
     #Move Clockwise
 
         while(angle != const):
             SendDat('l')
             const = getData()
             print("Current: ", const, "\nDir: ", angle, "\n")   
 
         SendDat('z')
 
     const = getData()'''

    # SendDat('1')
    print("Drive Forward")
    print("Current Position: ", arr, "\n")
    arr = cur()
    print("Dist: ", calc_dist(arr[0], arr[1], l2, lo2))
    time.sleep(1)
    # SendDat('z')

# SendDat('z')

# conn0.close()
# conn1.close()
print('Destination Reached\nHalt!')
