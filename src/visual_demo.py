import math
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots


ssDF = pd.read_csv(
    "C:\\Users\\OZGUN\\Documents\\GitHub\\iuc-mak-pro-i\\output\\single_slope_dataframe.csv")
ssDF.head()


# # ic ice girmis tek grafik
# for i in range(len(ssDF[ssDF['time_since_start'] == 0])):
#     fig = px.line(ssDF, x='time_since_start',
#                   y='elevation', color='ride_index')
# fig.show()


# # sub plot ile olusturulmus grafik ortak x axis
# total_ride_count = ssDF['ride_index'].iloc[-1]

# fig = make_subplots(rows=int(total_ride_count), cols=1)

# for i in ssDF['ride_index'].unique():
#     tour_name = "Tour " + str(i)
#     fig.append_trace(go.Scatter(
#         x=ssDF[ssDF['ride_index'] == i]['time_since_start'],
#         y=ssDF[ssDF['ride_index'] == i]['elevation'],
#         name=tour_name
#     ), row=i, col=1)
#     # Updating every single subplot's axes information.
#     fig.update_xaxes(title_text='Time (second)', row=i, col=1)
#     fig.update_yaxes(title_text='Elevation (meter)', row=i, col=1)
# fig.update_layout(height=600*total_ride_count, title_text="All Tour Graphs in One (Elevation-Time)")

# #fig.update_layout(height=600, width=600, title_text="Stacked Subplots")
# fig.show()

# slider menu
hover_text = []
bubble_size = []

ssDF = ssDF.sort_values('slope_percentage')
ssDF = ssDF[ssDF['distance_covered'] != 0]
ssDF = ssDF.reset_index(drop=True)

fig = px.scatter(
    ssDF, x="time_since_start", y="avg_velocity_kmh",
    animation_frame="slope_percentage",
    animation_group="ride_index",
    color="distance_since_start",
    size='total_climb_since_start',
    size_max=50,
    range_x=[-2000, 50000],
    range_y=[-3, 60],
    range_color=(0, 70000),
    template='ggplot2',
    color_continuous_scale=px.colors.sequential.Inferno
)
fig["layout"].pop("updatemenus")  # optional, drop animation buttons
# fig.show()

# toplu gösterim

fig = px.scatter(
    ssDF, x="time_since_start", y="avg_velocity_kmh",
    animation_group="ride_index",
    color="slope_percentage",
    size='distance_covered',
    size_max=60,
    range_x=[-2000, 50000],
    range_y=[-3, 60],
    range_color=(-6, 6),
    template='ggplot2',
    color_continuous_scale=px.colors.sequential.Inferno
)

fig["layout"].pop("updatemenus")  # optional, drop animation buttons


fig.show()
