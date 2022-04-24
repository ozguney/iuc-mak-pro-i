import os

from gpx_file_reader import GPXFile
from visualization import *
from math_calculations import *
from dataframe_operations import *

# Directory: ..\Documents\\GitHub\\iuc-mak-pro-i\\gpx_files'
gpx_folder = os.path.abspath("gpx_files")

# All gpx files in the gpx_files folder.
gpx_file_list = os.listdir(gpx_folder)

# Creating empty DataFrame list
ssDF_list = []

for i in range(len(gpx_file_list)):
    gpxFile = GPXFile(os.path.join(gpx_folder, gpx_file_list[i]))
    print(gpx_file_list[i])
    gpxDF = gpxFile.get_gpx_dataframe()
    if gpxDF.empty:
        print("This file dont have any time value.")
        continue
    else:
        # Calculating all DataFrames.
        gpxDF, grDF, ssDF = all_operations(gpxDF)
        # Every ssDF DataFrame is going to append to a list
        ssDF_list.append(ssDF)
        print(gpx_file_list[i]," process is succesfully completed.")

# Combine all single slope dataframes into one DataFrame.
ssDF_csv = pd.concat(ssDF_list, ignore_index=True)

# Writing
output_folder = os.path.abspath("output")

# Writing Single Slope DataFrame to a CSV file. Exporting to ..\Documents\\GitHub\\iuc-mak-pro-i\\output
ssDF_csv.to_csv(os.path.join(
    output_folder, r'single_slope_dataframe.csv'), encoding='utf-8')

# TODO try catch yapılanması (zaman olmayan GPX dosyaları için) - balaban turu
# TODO visualizing scriptinin düzenlenmesi. son csv dosyasının dünya haritasında işlenmesi
# TODO write scriptinin düzenlenmesi. içerisine html harita çıktılarının da eklenmesi.