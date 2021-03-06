from datetime import datetime
from numpy import datetime64
import pandas as pd
from math_calculations import *


def drop_time_duplicates(df):
    # Deleting duplicated time informations
    df.drop_duplicates(subset=['time'], keep=False)
    # Reset index
    df = df.reset_index(drop=True)
    return df


def define_data_type(df):
    df['lat'] = df['lat'].astype(float)
    df['lon'] = df['lon'].astype(float)
    df['ele'] = df['ele'].astype(float)
    df['time'] = df['time'].astype(datetime64)
    return df


def delta_dist_meters(df):
    df["deltaDistMeters"] = haversine_distance(df['lat'].shift(),
                                               df['lon'].shift(),
                                               df.loc[1:, 'lat'],
                                               df.loc[1:, 'lon'])
    return df


def drop_zero_meter_displacements(df):
    # Deleting 0 meter rows, not touching first row.
    df = df[df.deltaDistMeters != 0]
    # Resetting index values due to deleting 0 second rows
    df = df.reset_index(drop=True)
    return df


def delta_time_sec(df):
    # Returns time as a float(maybe integer but not as a time. eg: 65, not 1m5s)
    df["deltaTimeSeconds"] = (df.loc[1:, 'time'] - df['time'].shift()).apply(lambda row: row.total_seconds())
    df.loc[0, ["deltaTimeSeconds"]] = 0
    # This is here, due to: "A value is trying to be set on a copy of a slice from a DataFrame. Try using .loc[row_indexer,col_indexer] = value instead"
    df.loc[0, ["deltaDistMeters"]] = 0
    return df


def delta_ele_meters(df):
    df["deltaElevationMeters"] = df["ele"].diff()
    df.loc[0, ["deltaElevationMeters"]] = 0
    return df


def cumulative_time(df):
    df["cumTime"] = df["deltaTimeSeconds"].cumsum()
    return df


def velocity_kph(df):
    df["velocityKmPerHour"] = df["deltaDistMeters"] / df["deltaTimeSeconds"] * (3600.0 / 1000)
    df.loc[0, ["velocityKmPerHour"]] = 0
    return df


def velocity_kph_moving_average(df):
    df["velocityKmPerHour_ma100"] = df["velocityKmPerHour"].rolling(window=100).mean()
    df["velocityKmPerHour_ma20"] = df["velocityKmPerHour"].rolling(window=20).mean()
    return df


def local_min_max(df):
    n = 50  # number of points to be checked before and after
    df['min'] = df.iloc[argrelextrema(df.ele.values, np.less_equal, order=n)[0]]['ele']
    df['max'] = df.iloc[argrelextrema(df.ele.values, np.greater_equal, order=n)[0]]['ele']

    # Dropping duplicated min max values
    df = df[df['min'].shift() != df['min']]
    df = df[df['max'].shift() != df['max']]
    return df


def cumulative_elevation(df):
    df["cumElevation"] = df["deltaElevationMeters"].cumsum()
    return df


def cumulative_distance(df):
    df["cumDistance"] = df["deltaDistMeters"].cumsum()
    return df


def calculate_gradients(df):
    # This method also drops extreme values
    gradients = [0]
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
    # Resetting index values due to deleting nan rows
    df = df.reset_index(drop=True)
    return df


def tag_gradient_ranges(df):
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


def gradient_details(df):
    # This method returns another dataframe of every single bins's percentages, ele gains-lose etc.
    gradient_details = []

    for gr_range in df['gradientRange'].dropna().unique():
        # Keep that subset only
        subset = df[df['gradientRange'] == gr_range]

        # Statistics
        total_distance = subset['deltaDistMeters'].sum()
        pct_of_total_ride = (
            subset['deltaDistMeters'].sum() / df['deltaDistMeters'].sum()) * 100
        elevation_gain = subset[subset['deltaElevationMeters']
                                > 0]['deltaElevationMeters'].sum()
        elevation_lost = subset[subset['deltaElevationMeters']
                                < 0]['deltaElevationMeters'].sum()

        # Save results
        gradient_details.append({
            'gradient_range': gr_range,
            'total_distance': np.round(total_distance, 2),
            'pct_of_total_ride': np.round(pct_of_total_ride, 2),
            'elevation_gain': np.round(elevation_gain, 2),
            'elevation_lost': np.round(np.abs(elevation_lost), 2)
        })
    gradient_details_df = pd.DataFrame(gradient_details).sort_values(by='gradient_range').reset_index(drop=True)
    # This returns another dataframe
    return gradient_details_df


def listing_single_slopes(df):
    # Min, max values parsed.
    df_dumpmin = df.dropna(subset=['min'])
    df_dumpmax = df.dropna(subset=['max'])
    # All min, max values's indexes added to "indexes" array.
    indexes = df_dumpmin.index.tolist() + df_dumpmax.index.tolist()
    # Indexes sorted in ascending order.
    indexes.sort()
    single_slopes = []
    total_climb_since_start = 0

    # Statistics
    for i in range(len(indexes)-1):
        start_lat = df.iloc[indexes[i]]['lat']
        start_lon = df.iloc[indexes[i]]['lon']
        end_lat = df.iloc[indexes[i+1]]['lat']
        end_lon = df.iloc[indexes[i+1]]['lon']
        distance_covered = df.iloc[:indexes[i+1]]['deltaDistMeters'].sum() - df.iloc[:indexes[i]
                                                                                     ]['deltaDistMeters'].sum()
        distance_since_start = df.iloc[:indexes[i+1]]['deltaDistMeters'].sum()
        elevation_change = df.iloc[indexes[i+1]]['cumElevation'] - df.iloc[indexes[i]]['cumElevation']
        elevation = df.iloc[indexes[i]]['ele']
        pct_of_total_ride = (df['deltaDistMeters'].iloc[indexes[i]:indexes[i+1]
                                                        ].sum() / df['deltaDistMeters'].sum()) * 100
        elevation_gain = df.iloc[indexes[i]:indexes[i+1]][df['deltaElevationMeters'] > 0]['deltaElevationMeters'].sum()
        total_climb_since_start += elevation_gain
        elevation_lost = df.iloc[indexes[i]:indexes[i+1]][df['deltaElevationMeters'] < 0]['deltaElevationMeters'].sum()
        if i == 0:
            time_since_start = 0
        else:
            time_since_start = df.iloc[indexes[0]:indexes[i]]['deltaTimeSeconds'].sum()
        time_elapsed = df.iloc[indexes[i]:indexes[i+1]]['deltaTimeSeconds'].sum()
        avg_velocity_kmh = (distance_covered/time_elapsed) * (3600.0 / 1000)
        if elevation_change < 0:
            slope_percentage = (elevation_lost/distance_covered)*100
            if -1 < slope_percentage < 0:  # Getting rid of -0.00
                slope_percentage = 0
        elif elevation_change > 0:
            slope_percentage = (elevation_gain/distance_covered)*100
        else:  # Slope change = 0
            slope_percentage = 0

    # Save results
        single_slopes.append({
            'start_lat': start_lat,
            'start_lon': start_lon,
            'end_lat': end_lat,
            'end_lon': end_lon,
            'distance_covered': np.round(distance_covered, 2),
            'distance_since_start': np.round(distance_since_start, 2),
            'elevation_change': np.round(elevation_change, 2),
            'elevation': elevation,
            'time_since_start': time_since_start,
            'time_elapsed': time_elapsed,
            'pct_of_total_ride': np.round(pct_of_total_ride, 2),
            'elevation_gain': np.round(elevation_gain, 2),
            'elevation_lost': np.round(np.abs(elevation_lost), 2),
            'avg_velocity_kmh': np.round(avg_velocity_kmh, 2),
            'slope_percentage': np.around(slope_percentage),
            'total_climb_since_start': np.round(total_climb_since_start, 2)
        })
    ss_df = pd.DataFrame(single_slopes)
    # This function returns every single slope group's dataframe as a list with their information.
    return ss_df


def all_operations(df):
    '''
    Returns list of DataFrames.
        (0)gpxDF: GPX dataframe.
        (1)grDF : Gradient range dataframe.
        (2)ssDF : Single slope list's dataframe.
    '''
    gpxDF = drop_time_duplicates(df)
    gpxDF = define_data_type(gpxDF)
    gpxDF = delta_dist_meters(gpxDF)
    gpxDF = drop_zero_meter_displacements(gpxDF)
    gpxDF = delta_time_sec(gpxDF)
    gpxDF = delta_ele_meters(gpxDF)
    gpxDF = cumulative_time(gpxDF)
    gpxDF = velocity_kph(gpxDF)
    gpxDF = local_min_max(gpxDF)
    gpxDF = cumulative_elevation(gpxDF)
    gpxDF = cumulative_distance(gpxDF)
    gpxDF = calculate_gradients(gpxDF)
    gpxDF = tag_gradient_ranges(gpxDF)
    # gpxDF = velocity_kph_moving_average(gpxDF)
    grDF = gradient_details(gpxDF)
    ssDF = listing_single_slopes(gpxDF)

    return [gpxDF, grDF, ssDF]
