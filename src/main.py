import os

from gpx_file_reader import GPXFile
from visualization import *
from math_calculations import *
from dataframe_operations import *


# Directory operations
gpx_file_path = 'C:\\Users\\OZGUN\\Documents\\GitHub\\iuc-mak-pro-i\\gpx_files\\Afternoon_Ride.gpx'
gpxFile = GPXFile(gpx_file_path)
gpxFile.print_info()

# Converting to DataFrame.
gpxDF = gpxFile.get_gpx_dataframe()

# Calculating all DataFrames.
gpxDF, grDF, ssDF = all_operations(gpxDF)




