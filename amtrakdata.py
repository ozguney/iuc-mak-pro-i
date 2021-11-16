#amtrak tarafindan olusturulan gpx python scripti

import pandas as pd
from datetime import datetime
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from gpx_file_reader import GPXFile

gpx_file_path = 'Afternoon_Ride.gpx'
gpxFile = GPXFile(gpx_file_path)

gpxFile.print_info()
gpxDF = gpxFile.get_gpx_dataframe()

fig = go.Figure(data=go.Scattergeo(
        lon = gpxDF['lon'],
        lat = gpxDF['lat'],
        text = gpxDF['ele'],
        mode = 'markers',
        line = dict(width = 0.5,color = 'blue')
))

fig.update_layout(
        title = 'Amtrak train ride',
        geo_scope='usa',
    )

fig.show()

fig = px.line_3d(gpxDF, x="lon", y="lat", z="ele")
fig.add_trace(go.Scatter3d(
    x = [gpxDF['lon'].iloc[0]], 
    y = [gpxDF['lat'].iloc[0]],
    z = [gpxDF['ele'].iloc[0]],
    name = 'DC'
))

fig.add_trace(go.Scatter3d(
    x = [gpxDF['lon'].iloc[-1]], 
    y = [gpxDF['lat'].iloc[-1]],
    z = [gpxDF['ele'].iloc[-1]],
    name = 'NYC'
))

fig.update_layout(
    title = "Elevation vs lat,lon"
)
fig.show()

gpxDFElevationAbove0 = gpxDF[gpxDF['ele'] >= 0] 
fig = px.line_3d(gpxDFElevationAbove0, x="lon", y="lat", z="ele")
fig.add_trace(go.Scatter3d(
    x = [gpxDFElevationAbove0['lon'].iloc[0]], 
    y = [gpxDFElevationAbove0['lat'].iloc[0]],
    z = [gpxDFElevationAbove0['ele'].iloc[0]],
    name = 'DC'
))

fig.add_trace(go.Scatter3d(
    x = [gpxDFElevationAbove0['lon'].iloc[-1]], 
    y = [gpxDFElevationAbove0['lat'].iloc[-1]],
    z = [gpxDFElevationAbove0['ele'].iloc[-1]],
    name = 'NYC'
))

fig.update_layout(
    title = "Elevation vs lat,lon"
)
fig.show()

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
#test_dist_between()

# velocity calculation
gpxDF["deltaDistMeters"] = dist_between(gpxDF['lat'].shift(), gpxDF['lon'].shift(),
                                       gpxDF.loc[1:, 'lat'], gpxDF.loc[1:, 'lon'])
gpxDF["deltaTimeSeconds"] = (gpxDF.loc[1:, 'time'] - gpxDF['time'].shift()).apply(lambda row: row.total_seconds())
gpxDF["velocityMetersPerSecond"] = gpxDF["deltaDistMeters"] / gpxDF["deltaTimeSeconds"]
gpxDF["velocityMilesPerHour"] = gpxDF["velocityMetersPerSecond"] * (3600.0 / 1609.34)

gpxDFSpeedFiltered = gpxDF.loc[(gpxDF["velocityMilesPerHour"] >= 0) & (gpxDF["velocityMilesPerHour"] < 150)]
gpxDFSpeedFiltered.describe()

# Plot velocity

fig = px.line_3d(gpxDFSpeedFiltered, x="lon", y="lat", z="velocityMilesPerHour")
fig.add_trace(go.Scatter3d(
    x = [gpxDFSpeedFiltered['lon'].iloc[0]], 
    y = [gpxDFSpeedFiltered['lat'].iloc[0]],
    z = [gpxDFSpeedFiltered['velocityMilesPerHour'].iloc[0]],
    name = 'DC'
))

fig.add_trace(go.Scatter3d(
    x = [gpxDFSpeedFiltered['lon'].iloc[-1]], 
    y = [gpxDFSpeedFiltered['lat'].iloc[-1]],
    z = [gpxDFSpeedFiltered['velocityMilesPerHour'].iloc[-1]],
    name = 'NYC'
))

velocityColors = []
for i in range(0, len(gpxDFSpeedFiltered)):
    v = gpxDFSpeedFiltered['velocityMilesPerHour'].iloc[i]
    if v <= 50:
        color = 'red'
    elif 51 < v <= 100:
        color = 'yellow'
    elif 101 < v <= 150:
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
fig.show()

# Distribution of velocities with histogram
fig = px.histogram(gpxDFSpeedFiltered, x="velocityMilesPerHour", nbins=20)
fig.show()