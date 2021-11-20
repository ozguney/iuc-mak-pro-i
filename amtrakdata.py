import pandas as pd
from datetime import datetime
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from gpx_file_reader import GPXFile
import plotly.express as px
import gpxpy
import gpxpy.gpx
from gpxpy.geo import *
from gpxpy.gpx import *

#   Reading GPX File
gpx_file_path = 'Afternoon_Ride.gpx'
gpxFile = GPXFile(gpx_file_path)

gpxFile.print_info()
gpxDF = gpxFile.get_gpx_dataframe()

#   Initilazing Figure
fig = go.Figure(data=go.Scattergeo(
        lon = gpxDF['lon'],
        lat = gpxDF['lat'],
        text = gpxDF['ele'],
        mode = 'markers',
        line = dict(width = 0.5,color = 'blue')
))

#   Updating Figure's Layout
fig.update_layout(
        title = 'Afternoon Ride',
        geo_scope='world',
    )

#   Writing Figure to HTML
fig.write_html("01_WorldView.html")

#   Initilazing Figure
fig = px.line_3d(gpxDF, x="lon", y="lat", z="ele")

#   Adding Starting Point
fig.add_trace(go.Scatter3d(
    x = [gpxDF['lon'].iloc[0]], 
    y = [gpxDF['lat'].iloc[0]],
    z = [gpxDF['ele'].iloc[0]],
    name = 'Starting Point'
))

#   Adding Destination Point
fig.add_trace(go.Scatter3d(
    x = [gpxDF['lon'].iloc[-1]], 
    y = [gpxDF['lat'].iloc[-1]],
    z = [gpxDF['ele'].iloc[-1]],
    name = 'Destination Point'
))

#   Updating Layout Name
fig.update_layout(
    title = "Elevation vs lat,lon"
)

#   Writing Figure to HTML
fig.write_html("02_BoxView.html")

# haversine formula: takes degrees
def dist_between(lat1, lon1, lat2, lon2):
    R = 6371e3 #metres
    phi1 = lat1 * np.pi/180
    phi2 = lat2 * np.pi/180
    deltaPhi = (lat2-lat1) * np.pi/180
    deltaLambda = (lon2-lon1) * np.pi/180
    
    a = np.sin(deltaPhi/2)**2 + np.cos(phi1) * np.cos(phi2) * (np.sin(deltaLambda/2)**2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R * c # meters

def test_dist_between():
    lat1 = gpxDF['lat'].iloc[0]
    lon1 = gpxDF['lon'].iloc[0]
    lat2 = gpxDF['lat'].iloc[-1]
    lon2 = gpxDF['lon'].iloc[-1]
    d = dist_between(lat1, lon1, lat2, lon2)
    print("dist (meters): ", d)
    dMiles = d/1609.34
    print("dist (miles): ", dMiles)

# velocity calculation
gpxDF["deltaDistMeters"] = dist_between(gpxDF['lat'].shift(),
                                        gpxDF['lon'].shift(),
                                        gpxDF.loc[1:, 'lat'],
                                        gpxDF.loc[1:, 'lon'])
gpxDF["deltaTimeSeconds"] = (gpxDF.loc[1:, 'time'] - gpxDF['time'].shift()).apply(lambda row: row.total_seconds())
gpxDF["velocityMetersPerSecond"] = gpxDF["deltaDistMeters"] / gpxDF["deltaTimeSeconds"]
gpxDF["velocityMilesPerHour"] = gpxDF["velocityMetersPerSecond"] * (3600.0 / 1609.34)

gpxDFSpeedFiltered = gpxDF.loc[(gpxDF["velocityMilesPerHour"] >= 0) & (gpxDF["velocityMilesPerHour"] < 150)]

#   gpxDFSpeedFiltered HTML Output
print(gpxDFSpeedFiltered.describe())
gpxDFSpeedFiltered.describe().to_html("05_InformationsAboutRide.html")

# Plot velocity

fig = px.line_3d(gpxDFSpeedFiltered, x="lon", y="lat", z="velocityMetersPerSecond")
fig.add_trace(go.Scatter3d(
    x = [gpxDFSpeedFiltered['lon'].iloc[0]], 
    y = [gpxDFSpeedFiltered['lat'].iloc[0]],
    z = [gpxDFSpeedFiltered['velocityMetersPerSecond'].iloc[0]],
    name = 'Starting Point'
))

fig.add_trace(go.Scatter3d(
    x = [gpxDFSpeedFiltered['lon'].iloc[-1]], 
    y = [gpxDFSpeedFiltered['lat'].iloc[-1]],
    z = [gpxDFSpeedFiltered['velocityMetersPerSecond'].iloc[-1]],
    name = 'Destination Point'
))

velocityColors = []
for i in range(0, len(gpxDFSpeedFiltered)):
    v = gpxDFSpeedFiltered['velocityMetersPerSecond'].iloc[i]
    if v <= 1:
        color = 'red'
    elif 1 < v <= 3:
        color = 'yellow'
    elif 3 < v <= 50:
        color = 'green'
    else:
        color = 'black'
    velocityColors.append(color)

fig.add_trace(go.Scatter3d(
    x = gpxDFSpeedFiltered['lon'], 
    y = gpxDFSpeedFiltered['lat'],
    z = [0 for n in range(len(gpxDFSpeedFiltered))],
    name = 'Route',
    line=dict(color=velocityColors, width=0)
))
    
fig.update_layout(
    title = "Velocity vs lat,lon"
)
fig.write_html("03_Velocity.html")

# Distribution of velocities with histogram
fig = px.histogram(gpxDFSpeedFiltered, x="velocityMetersPerSecond", nbins=20)
fig.write_html("04_Histogram.html")

# Creating Location Array

ride_loc = []

iteration=0
for element in gpxDFSpeedFiltered:
    ride_loc.append(Location(gpxDFSpeedFiltered['lat'].iloc[iteration], gpxDFSpeedFiltered['lon'].iloc[iteration], gpxDFSpeedFiltered['ele'].iloc[iteration]))
    iterasyon = iterasyon+1

# Grouping Slopes in an Array

iteration=0

tempAngleIndex = 0
currentAngleIndex = 0
tempAngle = elevation_angle(ride_loc[iteration], ride_loc[iteration+1])
currentAngle = elevation_angle(ride_loc[iteration], ride_loc[iteration+1])