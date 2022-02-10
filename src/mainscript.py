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

#   Reading GPX File
gpx_file_path = 'C:\\Users\\OZGUN\\Documents\\GitHub\\iuc-mak-pro-i\\gpx_files\\Afternoon_Ride.gpx'
gpxFile = GPXFile(gpx_file_path)

gpxFile.print_info()
gpxDF = gpxFile.get_gpx_dataframe()