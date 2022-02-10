import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Initilazing Figure
def MapBox(df):
    fig = go.Figure(go.Scattermapbox(
        mode = "markers+lines",
        lon = df['lon'],
        lat = df['lat'],
        marker = {'size': 10}))

    fig.add_trace(go.Scattermapbox(
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
            'zoom': 1})

    return fig