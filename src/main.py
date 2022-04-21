from gpx_file_reader import GPXFile
from visualization import *
from math_calculations import *
from dataframe_operations import *


# Reading and parsing GPX file.
gpx_file_path = 'C:\\Users\\OZGUN\\Documents\\GitHub\\iuc-mak-pro-i\\gpx_files\\Afternoon_Ride.gpx'
gpxFile = GPXFile(gpx_file_path)
gpxFile.print_info()

# Converting to DataFrame.
gpxDF = gpxFile.get_gpx_dataframe()
print("Dataframe succesfully created by GPX file.")

all_dataframes = all_operations(gpxDF)

gpxDF = all_dataframes[0]
grDF = all_dataframes[1]
ssDF = all_dataframes[2]

gpxDF
grDF
ssDF

# gpxDF_10 = gpxDF[gpxDF.index % 10 == 0] # Getting 1 row from every 10 row. Make calculations more smooth

# Calculating speed, distance etc.
# 
# gpxDF = DataFrameCalculations(gpxDF)
# gpxDF = DataFrameSmoothing(gpxDF)
# gpxDF = GroupSlopes(gpxDF)
# gpxDF = CumulativeElevationDistance(gpxDF)
# gpxDF = ElevationGradients(gpxDF)
# gpxDF["elevationGradients"] = gpxDF["elevationGradients"].fillna(0)
# gpxDF = GradientRangeTagging(gpxDF)
# gpxDF_RangeDetails = GradientRangeTagDetails(gpxDF)
# ssDF = SingleSlopeGroups(gpxDF)

#----- visualization --------------------------------------------------------------------#

# pio.renderers.default = "notebook_connected"
pio.renderers.default = "browser"

# fig_MapBox = visualization.MapBox(gpxDF)
# fig_MapBox.show()
# fig_Scatter3d = visualization.Scatter3d(gpxDF)
# fig_Scatter3d.show()
# fig_Scatter3dVelocity = visualization.Scatter3dVelocity(gpxDF)
# fig_Scatter3dVelocity.show()
# fig_VelocityTimeGraph_ma100 = visualization.VelocityTimeGraph_ma100(gpxDF)
# fig_VelocityTimeGraph_ma100.show()
# fig_VelocityTimeGraphMaComparison = visualization.VelocityTimeGraphMaComparison(gpxDF)
# fig_VelocityTimeGraphMaComparison.show()
# fig_ElevationTimeGraph = visualization.ElevationTimeGraph(gpxDF)
# fig_ElevationTimeGraph.show()
# fig_VelocityElevationCombined = visualization.VelocityElevationCombined(gpxDF)
# fig_VelocityElevationCombined.show()

# fig_GradientRangeGraph = visualization.GradientRangeGraph(gpxDF_RangeDetails)
# fig_GradientRangeGraph.show()

# fig_VelocityHeatMap = visualization.VelocityHeatMap(gpxDF)
# fig_VelocityHeatMap.show()

# fig_ElevationMinMaxPoints = ElevationMinMaxPoints(gpxDF)
# fig_ElevationMinMaxPoints.show()


# SIRALAMA DEGISTIGI ICIN BU ISLEVSIZ KALACAKTIR ILOC YERINE LOC KULLANILMALI
# for i in range(len(ssDF)-1):   # for each row:
#     # plt.plot([list of Xs], [list of Ys])
#     plt.plot([ssDF.iloc[i, 7], ssDF.iloc[i+1, 7]],
#              [ssDF.iloc[i, 6], ssDF.iloc[i+1, 6]])
# plt.show()

#---------------------------------------------------------------------------------------#


#----- WRITING -----#

# fig_MapBox.write_html("fig_MapBox.html")
# fig_Scatter3d.write_html("fig_Scatter3d.html")
# fig_Scatter3dVelocity.write_html("fig_Scatter3dVelocity.html")
# fig_VelocityTimeGraph.write_html("fig_VelocityTimeGraph.html")
# fig_ElevationTimeGraph.write_html("fig_ElevationTimeGraph.html")
# fig_VelocityElevationCombined.write_html("fig_VelocityElevationCombined.html")
# fig_VelocityHeatMap.write_html("fig_VelocityHeatMap.html")

#---------------------------------------------------------------------------------------#
