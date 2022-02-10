from lib2to3.pgen2.pgen import DFAState
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def MapBox(df):
    #todo marker ve line düzenlemesi. zoom düzenlemesi. center düzenlemesi. başlangıç bitiş noktasının ayarlanması
    fig = go.Figure(go.Scattermapbox(
        mode = "markers+lines",
        lon = df['lon'],
        lat = df['lat'],
        marker = {'size': 10}))

    fig.update_layout(
        margin ={'l':0,'t':0,'b':0,'r':0},
        mapbox = {
            'center': {'lon': 10, 'lat': 10},
            'style': "stamen-terrain",
            'center': {'lon': -20, 'lat': -20},
            'zoom': 0})
    return fig

def Scatter3d(df):
    #   Initilazing Figure
    fig = px.line_3d(df, x="lon", y="lat", z="ele")

    #   Adding Starting Point
    fig.add_trace(go.Scatter3d(
        x = [df['lon'].iloc[0]], 
        y = [df['lat'].iloc[0]],
        z = [df['ele'].iloc[0]],
        name = 'Starting Point', 
    ))

    #   Adding Destination Point
    fig.add_trace(go.Scatter3d(
        x = [df['lon'].iloc[-1]], 
        y = [df['lat'].iloc[-1]],
        z = [df['ele'].iloc[-1]],
        name = 'Destination Point'
    ))

    #   Updating Layout Name
    fig.update_layout(
        title = "Elevation vs lat,lon"
    )
    return fig

def Scatter3dVelocity(df):
    fig = px.line_3d(df, x="lon", y="lat", z="velocityKmPerHour")
    fig.add_trace(go.Scatter3d(
    x = [df['lon'].iloc[0]], 
    y = [df['lat'].iloc[0]],
    z = [df['velocityKmPerHour'].iloc[0]],
    name = 'Starting Point'
    ))

    fig.add_trace(go.Scatter3d(
    x = [df['lon'].iloc[-1]], 
    y = [df['lat'].iloc[-1]],
    z = [df['velocityKmPerHour'].iloc[-1]],
    name = 'Destination Point'
    ))

    velocityColors = []
    for i in range(0, len(df)):
        v = df['velocityKmPerHour'].iloc[i]
        if v <= 1:
            color = 'red'
        elif 1 < v <= 10:
            color = 'yellow'
        elif 10 < v <= 50:
            color = 'green'
        else:
            color = 'black'
        velocityColors.append(color)

    fig.add_trace(go.Scatter3d(
    x = df['lon'], 
    y = df['lat'],
    z = [0 for n in range(len(df))],
    name = 'Route',
    line=dict(color=velocityColors, width=0)
    ))
    
    fig.update_layout(
    title = "Velocity vs lat,lon"
    )
    return fig

def Velocity2d(df):
    return 0
def HeatMap(df):
    return 0