import pandas as pd # pandas 1.3.5
import numpy as np # numpy 1.22.2
import gpxpy
import gpxpy.gpx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import visualizing
from gpx_file_reader import GPXFile
from datetime import datetime
from gpxpy.geo import *
from gpxpy.gpx import *
from scipy.signal import argrelextrema

def dist_between(lat1, lon1, lat2, lon2):
    R = 6371e3 #metres
    phi1 = lat1 * np.pi/180
    phi2 = lat2 * np.pi/180
    deltaPhi = (lat2-lat1) * np.pi/180
    deltaLambda = (lon2-lon1) * np.pi/180
    
    a = np.sin(deltaPhi/2)**2 + np.cos(phi1) * np.cos(phi2) * (np.sin(deltaLambda/2)**2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R * c # meters
def ElevationAngle(ele1, ele2, distance):
    return np.arctan((ele2-ele1)/distance)
def DataFrameCalculations(df):
    df.drop_duplicates(subset=['time'], keep=False) # Deleting duplicated times
    df["deltaDistMeters"] = dist_between(df['lat'].shift(),
                                        df['lon'].shift(),
                                        df.loc[1:, 'lat'],
                                        df.loc[1:, 'lon'])
    df["deltaElevationMeters"] = df["ele"].diff()
    df["elevationAngle"] = ElevationAngle(df['ele'].shift(),
                                          df.loc[1:, 'ele'],
                                          df["deltaDistMeters"])

    df["deltaTimeSeconds"] = (df.loc[1:, 'time'] - df['time'].shift()).apply(lambda row: row.total_seconds())
    df = df[df.deltaDistMeters != 0] # Deleting 0 meter rows
    df = df.reset_index(drop=True) # Resetting index values due to deleting 0 second rows
    df["velocityKmPerHour"] = df["deltaDistMeters"] / df["deltaTimeSeconds"] * (3600.0 / 1000)
    df = df[df.velocityKmPerHour < 50]
    df = df.reset_index(drop=True)
    return df
def DataFrameSmoothing(df):
    df["velocityKmPerHour_ma100"] = df["velocityKmPerHour"].rolling(window=100).mean()
    df["velocityKmPerHour_ma20"] = df["velocityKmPerHour"].rolling(window=20).mean()
    return df
def GroupSlopes(df):
    n = 50 # number of points to be checked before and after
    df['min'] = df.iloc[argrelextrema(df.ele.values, np.less_equal,order=n)[0]]['ele']
    df['max'] = df.iloc[argrelextrema(df.ele.values, np.greater_equal,order=n)[0]]['ele']
    
    df = df[df['min'].shift() != df['min']] # Dropping duplicated min max values
    df = df[df['max'].shift() != df['max']]
    '''
    df_dumpmin = df.dropna(subset=['min']) # Dropping between values
    df_dumpmax = df.dropna(subset=['max'])
    df_dumpmin.index.tolist()
    df_dumpmax.index.tolist()
    dumplist = df_dumpmin.index.tolist() + df_dumpmax.index.tolist()
    dumplist.sort()
    df['selectedIndexes'] = pd.Series(dumplist)
    '''
    return df
def CumulativeElevationDistance(df):
    df["cumElevation"] = df["deltaElevationMeters"].cumsum()
    df["cumDistance"] = df["deltaDistMeters"].cumsum()
    return df
def ElevationGradients(df):
    gradients = [np.nan]
    for ind, row in df.iterrows():
        if ind == 0:
            continue
        grade = (row["deltaElevationMeters"]/row["deltaDistMeters"]) * 100
        if grade > 30:
            gradients.append(np.nan)
        elif grade < -30:
            gradients.append(np.nan)
        else:
            gradients.append(np.round(grade, 1))
    df["elevationGradients"] = gradients
    return df
def GradientRangeTagging(df):
    bins = pd.IntervalIndex.from_tuples([
    (-30, -10),
    (-10, -5), 
    (-5, -3), 
    (-3, -1), 
    (-1, 1),
    (1, 3), 
    (3, 5), 
    (5, 10), 
    (10, 30)],
    closed='right')
    df["gradientRange"] = pd.cut(df["elevationGradients"], bins=bins)
    return df
def GradientRangeTagDetails(df):
    gradient_details = []

    for gr_range in df['gradientRange'].unique():
        # Keep that subset only
        subset = df[df['gradientRange'] == gr_range]
        
        # Statistics
        total_distance = subset['deltaDistMeters'].sum()
        pct_of_total_ride = (subset['deltaDistMeters'].sum() / df['deltaDistMeters'].sum()) * 100
        elevation_gain = subset[subset['deltaElevationMeters'] > 0]['deltaElevationMeters'].sum()
        elevation_lost = subset[subset['deltaElevationMeters'] < 0]['deltaElevationMeters'].sum()
        
        # Save results
        gradient_details.append({
            'gradient_range': gr_range,
            'total_distance': np.round(total_distance, 2),
            'pct_of_total_ride': np.round(pct_of_total_ride, 2),
            'elevation_gain': np.round(elevation_gain, 2),
            'elevation_lost': np.round(np.abs(elevation_lost), 2)
        })
    gradient_details_df = pd.DataFrame(gradient_details).sort_values(by='gradient_range').reset_index(drop=True)
    return gradient_details_df
def SingleSlopeGroups(df):
    df_dumpmin = df.dropna(subset=['min'])
    df_dumpmax = df.dropna(subset=['max'])
    df_dumpmin.index.tolist()
    df_dumpmax.index.tolist()
    indexes = df_dumpmin.index.tolist() + df_dumpmax.index.tolist()
    indexes.sort()

    data = {'start_lat': [],
            'start_lon': [],
            'end_lat': [],
            'end_lon': [],
            'distance_covered': [],
            'elevation_change': [],
            'time_since_start': [],
            'time_elapsed': []
            }
    ss_df = pd.DataFrame(data)
    
    for index in indexes:
        df.
    return df # This function returns every single slope group's dataframe for own purpose.
# Reading and parsing GPX file.
gpx_file_path = 'C:\\Users\\OZGUN\\Documents\\GitHub\\iuc-mak-pro-i\\gpx_files\\Afternoon_Ride.gpx'
gpxFile = GPXFile(gpx_file_path)
gpxFile.print_info()

# Converting to DataFrame.
gpxDF = gpxFile.get_gpx_dataframe()
# gpxDF_10 = gpxDF[gpxDF.index % 10 == 0] # Getting 1 row from every 10 row. Make calculations more smooth

#Calculating speed, distance etc.
gpxDF = DataFrameCalculations(gpxDF)
gpxDF = DataFrameSmoothing(gpxDF)
gpxDF = GroupSlopes(gpxDF)
gpxDF = CumulativeElevationDistance(gpxDF)
gpxDF = ElevationGradients(gpxDF)
gpxDF["elevationGradients"] = gpxDF["elevationGradients"].fillna(0)
gpxDF = GradientRangeTagging(gpxDF)
gpxDF_RangeDetails = GradientRangeTagDetails(gpxDF)

#### VISUALIZING ####

# pio.renderers.default = "notebook_connected"
pio.renderers.default = "browser"

# fig_MapBox = visualizing.MapBox(gpxDF)
# fig_MapBox.show()
# fig_Scatter3d = visualizing.Scatter3d(gpxDF)
# fig_Scatter3d.show()
# fig_Scatter3dVelocity = visualizing.Scatter3dVelocity(gpxDF)
# fig_Scatter3dVelocity.show()
# fig_VelocityTimeGraph_ma100 = visualizing.VelocityTimeGraph_ma100(gpxDF)
# fig_VelocityTimeGraph_ma100.show()
# fig_VelocityTimeGraphMaComparison = visualizing.VelocityTimeGraphMaComparison(gpxDF)
# fig_VelocityTimeGraphMaComparison.show()
# fig_ElevationTimeGraph = visualizing.ElevationTimeGraph(gpxDF)
# fig_ElevationTimeGraph.show()
# fig_VelocityElevationCombined = visualizing.VelocityElevationCombined(gpxDF)
# fig_VelocityElevationCombined.show()

# fig_GradientRangeGraph = visualizing.GradientRangeGraph(gpxDF_RangeDetails)
# fig_GradientRangeGraph.show()

# fig_VelocityHeatMap = visualizing.VelocityHeatMap(gpxDF)
# fig_VelocityHeatMap.show()

fig_ElevationMinMaxPoints = visualizing.ElevationMinMaxPoints(gpxDF)
fig_ElevationMinMaxPoints.show()

#### WRITING ####

# fig_MapBox.write_html("fig_MapBox.html")
# fig_Scatter3d.write_html("fig_Scatter3d.html")
# fig_Scatter3dVelocity.write_html("fig_Scatter3dVelocity.html")
# fig_VelocityTimeGraph.write_html("fig_VelocityTimeGraph.html")
# fig_ElevationTimeGraph.write_html("fig_ElevationTimeGraph.html")
# fig_VelocityElevationCombined.write_html("fig_VelocityElevationCombined.html")
# fig_VelocityHeatMap.write_html("fig_VelocityHeatMap.html")