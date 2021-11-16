import pandas as pd
from datetime import datetime
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from gpx_file_reader import GPXFile
import plotly.express as px

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