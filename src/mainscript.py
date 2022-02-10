import pandas as pd
import numpy as np
import gpxpy
import gpxpy.gpx
import plotly.graph_objects as go
import plotly.express as px
from gpx_file_reader import GPXFile
from datetime import datetime
from gpxpy.geo import *
from gpxpy.gpx import *

# Reading and parsing GPX file.
gpx_file_path = 'C:\\Users\\OZGUN\\Documents\\GitHub\\iuc-mak-pro-i\\gpx_files\\Afternoon_Ride.gpx'
gpxFile = GPXFile(gpx_file_path)
gpxFile.print_info()

# Converting to DataFrame.
gpxDF = gpxFile.get_gpx_dataframe()

def dist_between(lat1, lon1, lat2, lon2):
    R = 6371e3 #metres
    phi1 = lat1 * np.pi/180
    phi2 = lat2 * np.pi/180
    deltaPhi = (lat2-lat1) * np.pi/180
    deltaLambda = (lon2-lon1) * np.pi/180
    
    a = np.sin(deltaPhi/2)**2 + np.cos(phi1) * np.cos(phi2) * (np.sin(deltaLambda/2)**2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R * c # meters

gpxDF["deltaDistMeters"] = dist_between(gpxDF['lat'].shift(),
                                        gpxDF['lon'].shift(),
                                        gpxDF.loc[1:, 'lat'],
                                        gpxDF.loc[1:, 'lon'])

gpxDF["deltaTimeSeconds"] = (gpxDF.loc[1:, 'time'] - gpxDF['time'].shift()).apply(lambda row: row.total_seconds())
gpxDF = gpxDF[gpxDF.deltaTimeSeconds != 0] # Deleting 0 second rows
