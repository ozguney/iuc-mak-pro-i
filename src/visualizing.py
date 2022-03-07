from turtle import fillcolor
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def MapBox(df):
    #todo başlangıç bitiş noktasının ayarlanması
    fig = go.Figure(go.Scattermapbox(
        mode = "markers+lines",
        lon = df['lon'],
        lat = df['lat'],
        marker = {'size': 10}))

    fig.update_layout(
        margin ={'l':0,'t':0,'b':0,'r':0},
        mapbox = {
            'center': {'lon': df['lon'].iloc[0], 'lat': df['lat'].iloc[0]},
            'style': "stamen-terrain",
            'zoom': 12})
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

def VelocityTimeGraph_ma100(df):
    fig = px.line(df, 
                  x=df["time"], 
                  y=df["velocityKmPerHour_ma100"], 
                  title='Velocity - Time Graph')
    return fig

def VelocityTimeGraphMaComparison(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["time"], y=df["velocityKmPerHour"],
                        mode='lines',
                        name='Raw Data'))
    fig.add_trace(go.Scatter(x=df["time"], y=df["velocityKmPerHour_ma20"],
                        mode='lines',
                        name='Moving Average (20)'))
    fig.add_trace(go.Scatter(x=df["time"], y=df["velocityKmPerHour_ma100"],
                        mode='lines', 
                        name='Moving Average (100)'))
    return fig

def VelocityHeatMap(df):
    # data fazlaligindan dolayi yavas olan yerleri daha yogun gosterdigi icin veri olan fazla kismi sari gosteriyor
    fig = go.Figure(go.Densitymapbox(
        lon = df['lon'],
        lat = df['lat'],
        z = df["velocityKmPerHour_ma"],
        radius=10))
    fig.update_layout(mapbox = {
            'center': {'lon': df['lon'].iloc[0], 'lat': df['lat'].iloc[0]},
            'style': "stamen-terrain",
            'zoom': 14})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def ElevationTimeGraph(df):
    fig = px.line(df, x=df["time"], y=df["ele"], title='Elevation - Time Graph')
    return fig

def VelocityElevationCombined(df):
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=df["time"], y=df["ele"], name="Elevation"),
        secondary_y=False)
    fig.add_trace(
        go.Scatter(x=df["time"], y=df["velocityKmPerHour_ma"], name="Velocity kmh"),
        secondary_y=True)
    fig.update_layout(title_text="Elevation Velocity Combined Graph")
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="Elevation", secondary_y=False)
    fig.update_yaxes(title_text="Velocity kmh", secondary_y=True)
    # fig.update_traces(line_shape='spline') # Tried data smoothing but not worked the way that i wanted.
    return fig

