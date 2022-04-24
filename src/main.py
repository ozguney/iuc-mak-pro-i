import os

from gpx_file_reader import GPXFile
from visualization import *
from math_calculations import *
from dataframe_operations import *

# Directory: ..\Documents\\GitHub\\iuc-mak-pro-i\\gpx_files'
gpx_folder = os.path.abspath("gpx_files")

# All gpx files in the gpx_files folder.
gpx_file_list = os.listdir(gpx_folder)

# Creating empty lists
ssDF_list, no_time_info_file_list = [], []

# Ride index used to index each file in ssDF.
ride_index = 1

for i in range(len(gpx_file_list)):
    gpxFile = GPXFile(os.path.join(gpx_folder, gpx_file_list[i]))
    print(f"Analyzing: {gpx_file_list[i]}")
    gpxDF = gpxFile.get_gpx_dataframe()
    if gpxDF.empty:
        print(
            f"ERROR: This file dont have time component. This GPX file will not be processed: {gpx_file_list[i]}")
        no_time_info_file_list.append(gpx_file_list[i])
    else:
        # Calculating all DataFrames.
        gpxDF, grDF, ssDF = all_operations(gpxDF)
        # Adding ride index to first row of DataFrame.
        ssDF.insert(0, 'ride_index', pd.Series([ride_index for x in range(len(ssDF.index))]))
        ride_index = ride_index + 1
        # Every ssDF DataFrame is going to append to a list
        ssDF_list.append(ssDF)
        print("Analysis finished succesfully.")

# Debugging...
print(f"These files were not processed because they do not contain time information: {no_time_info_file_list}")

# Combine all single slope dataframesss into one DataFrame.
ssDF_csv = pd.concat(ssDF_list, ignore_index=True)

# Writing to file.
output_folder = os.path.abspath("output")

# Writing Single Slope DataFrame to a CSV file. Exporting to ..\Documents\\GitHub\\iuc-mak-pro-i\\output
ssDF_csv.to_csv(os.path.join(
    output_folder, r'single_slope_dataframe.csv'), encoding='utf-8', index=False)

# TODO visualizing scriptinin düzenlenmesi. son csv dosyasının dünya haritasında işlenmesi
# TODO write scriptinin düzenlenmesi. içerisine html harita çıktılarının da eklenmesi.
