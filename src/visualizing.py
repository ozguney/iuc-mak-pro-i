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
                        line=dict(width=1),
                        name='Raw Data'))
    fig.add_trace(go.Scatter(x=df["time"], y=df["velocityKmPerHour_ma20"],
                        mode='lines',
                        line=dict(width=2),
                        name='Moving Average (20)'))
    fig.add_trace(go.Scatter(x=df["time"], y=df["velocityKmPerHour_ma100"],
                        mode='lines',
                        line=dict(width=5), 
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

def ElevationMinMaxPoints(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["time"], 
                            y=df["ele"],
                            mode='lines',
                            name='Elevation'))
    fig.add_trace(go.Scatter(x=df["time"],
                            y=df['min'],
                            mode='markers',
                            marker=dict(color="red", size=10),
                            name='Minimum Value'))
    fig.add_trace(go.Scatter(x=df["time"],
                            y=df['max'],
                            mode='markers',
                            marker=dict(color="green", size=10), 
                            name='Maximum Value'))
    return fig

def GradientRangeGraph(df):
    colors = [
        '#0d46a0', '#2f3e9e', '#2195f2', '#4fc2f7',
        '#a5d6a7', '#66bb6a', '#fff59d', '#ffee58',
        '#ffca28', '#ffa000', '#ff6f00', '#f4511e', '#bf360c'
    ]
    custom_text = [f'''<b>{gr}%</b> - {dst}km''' for gr, dst in zip(
        df['gradient_range'].astype('str'),
        df['total_distance'].apply(lambda x: round(x / 1000, 2))
    )]
    fig = go.Figure(
        data=[go.Bar(
            x=df['gradient_range'].astype(str),
            y=df['total_distance'].apply(lambda x: round(x / 1000, 2)),
            marker_color=colors,
            text=custom_text
        )],
        layout=go.Layout(
            bargap=0,
            title='Gradient profile of a route',
            xaxis_title='Gradient range (%)',
            yaxis_title='Distance covered (km)',
            autosize=False,
            width=1440,
            height=800,
            template='simple_white'
        )
    )
    return fig