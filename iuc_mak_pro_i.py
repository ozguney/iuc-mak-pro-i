import gpxpy
import gpxpy.gpx
from gpxpy.geo import *
from gpxpy.gpx import *

from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

ride_lat = []
ride_lon = []
ride_ele = []
ride_time = []
ride_loc = []

gpx_file = open("Afternoon_Ride.gpx","r")
ride = gpxpy.parse(gpx_file)
for track in ride.tracks:
    for segment in track.segments:
        for point in segment.points:
            ride_lat.append(point.latitude)
            ride_lon.append(point.longitude)
            ride_ele.append(point.elevation)
            ride_time.append(point.time)

# Location atamalarinin yapildigi yer.
iterasyon=0
for element in ride_time:
    ride_loc.append(Location(ride_lat[iterasyon], ride_lon[iterasyon], ride_ele[iterasyon]))
    iterasyon = iterasyon+1

#===== Writing in a file operations =====#

# f = open("demo_lat.txt", "a+")
# f.write(str(ride_lat) + "\n")
# f.close()

#----- haversine_distance -----#
# Haversine distance between two points, expressed in meters.

haversine = haversine_distance(ride_lat[0], ride_lon[0],ride_lat[1], ride_lon[1])
print("haversine_distance:\n",haversine,"meters")

#----- get_course -----#
# Returning a route, expressed in meters.

getcourse = get_course(ride_lat[0], ride_lon[0],ride_lat[1], ride_lon[1])
print("get course:\n",haversine,"meters")

#----- elevation_angle -----#
# Uphill/downhill angle between two locations, expressed in degrees(can be positive or negative).

elevationangle = elevation_angle(ride_loc[0], ride_loc[500])
print("Elevation angle:\n",elevationangle,"degrees")

#==========================================================================
# https://www.pythonpool.com/python-string-to-variable-name/

counter = 1

def GroupSlopes():
    global counter # accessing the counter variable that outside of def
    dynamic_variable = "slope_"+str(counter)
    globals()[dynamic_variable] = []
    counter = counter + 1

# slope karsilastirmasi
angle_first = elevation_angle(ride_loc[0], ride_loc[1])
slope_group=[[]]
slope_group_depth = 0

for i in range(len(ride_ele)-1):

    angle_second = elevation_angle(ride_loc[i], ride_loc[i+1])
    angle_dif = angle_second - angle_first

    if(angle_dif >= 0 and angle_dif<1): # aci farki 0 ve 1 arasinda ise
        slope_group[slope_group_depth].append(ride_loc[i])

    elif(angle_dif>=1): # aci farki 1'den buyukse yeni depth olusturacak kod
        angle_first = elevation_angle(ride_loc[i], ride_loc[i+1]) # 1 dereceden büyükse atanan yeni angle first degeri
        slope_group[slope_group_depth].append(ride_loc[i]) # son deger aktarildi
        slope_group.append([])
        slope_group_depth += 1 # depth arttirildi. atamada yeni olan grubun icerisine aktariliyor artik
    elif(angle_dif):
        a=3

    





#==========================================================================


# MatPlotLib Komutlari (2D)
t1 = np.arange(0.0, 333.5, 0.1)
plt.plot(t1, ride_ele, label = "Yukseklik")
# time ve ele kodu calismamakta. plt.plot(ride_time, ride_ele, label = "Yukseklik")

# MatPlotLib Komutlari (3D)
fig = plt.figure()
ax = plt.axes(projection='3d')
plt.show()