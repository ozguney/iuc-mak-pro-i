import pandas as pd
from math_calculations import *
from pandas.core.base import PandasObject



def DataFrameCalculations(df):
    # Deleting duplicated times
    df.drop_duplicates(subset=['time'], keep=False)
    df["deltaDistMeters"] = haversine_distance(df['lat'].shift(),
                                               df['lon'].shift(),
                                               df.loc[1:, 'lat'],
                                               df.loc[1:, 'lon'])
    df["deltaElevationMeters"] = df["ele"].diff()
    df["elevationAngle"] = elevation_angle(df['ele'].shift(),
                                           df.loc[1:, 'ele'],
                                           df["deltaDistMeters"])

    df["deltaTimeSeconds"] = (
        df.loc[1:, 'time'] - df['time'].shift()).apply(lambda row: row.total_seconds())
    df["cumTime"] = df["deltaTimeSeconds"].cumsum()
    df = df[df.deltaDistMeters != 0]  # Deleting 0 meter rows
    # Resetting index values due to deleting 0 second rows
    df = df.reset_index(drop=True)
    df["velocityKmPerHour"] = df["deltaDistMeters"] / \
        df["deltaTimeSeconds"] * (3600.0 / 1000)
    df = df[df.velocityKmPerHour < 50]
    df = df.reset_index(drop=True)
    return df

def your_fun(df):

    return df
PandasObject.your_fun = your_fun

def drop_time_duplicates(df):
    # Deleting duplicated times
    df.drop_duplicates(subset=['time'], keep=False)
    df = df.reset_index(drop=True)
    return df
PandasObject.drop_time_duplicates = drop_time_duplicates

def DataFrameSmoothing(df):
    df["velocityKmPerHour_ma100"] = df["velocityKmPerHour"].rolling(
        window=100).mean()
    df["velocityKmPerHour_ma20"] = df["velocityKmPerHour"].rolling(
        window=20).mean()
    return df


def GroupSlopes(df):
    n = 50  # number of points to be checked before and after
    df['min'] = df.iloc[argrelextrema(
        df.ele.values, np.less_equal, order=n)[0]]['ele']
    df['max'] = df.iloc[argrelextrema(
        df.ele.values, np.greater_equal, order=n)[0]]['ele']

    # Dropping duplicated min max values
    df = df[df['min'].shift() != df['min']]
    df = df[df['max'].shift() != df['max']]
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
    # Resetting index values due to deleting nan rows
    df = df.reset_index(drop=True)
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
    gradient_details_df = pd.DataFrame(gradient_details).sort_values(
        by='gradient_range').reset_index(drop=True)
    return gradient_details_df


def SingleSlopeGroups(df):
    df_dumpmin = df.dropna(subset=['min'])
    df_dumpmax = df.dropna(subset=['max'])
    df_dumpmin.index.tolist()
    df_dumpmax.index.tolist()
    indexes = df_dumpmin.index.tolist() + df_dumpmax.index.tolist()
    indexes.sort()

    single_slopes = []

    for i in range(len(indexes)-1):
        start_lat = df.iloc[indexes[i]]['lat']
        start_lon = df.iloc[indexes[i]]['lon']
        end_lat = df.iloc[indexes[i+1]]['lat']
        end_lon = df.iloc[indexes[i+1]]['lon']
        distance_covered = df.iloc[indexes[i+1]
                                   ]['cumDistance'] - df.iloc[indexes[i]]['cumDistance']
        elevation_change = df.iloc[indexes[i+1]
                                   ]['cumElevation'] - df.iloc[indexes[i]]['cumElevation']
        elevation = df.iloc[indexes[i]]['ele']
        time_since_start = df.iloc[indexes[i]]['cumTime']
        time_elapsed = df.iloc[indexes[i+1]]['cumTime'] - \
            df.iloc[indexes[i]]['cumTime']

        single_slopes.append({
            'start_lat': start_lat,
            'start_lon': start_lon,
            'end_lat': end_lat,
            'end_lon': end_lon,
            'distance_covered': distance_covered,
            'elevation_change': elevation_change,
            'elevation': elevation,
            'time_since_start': time_since_start,
            'time_elapsed': time_elapsed
        })
    ss_df = pd.DataFrame(single_slopes)
    # This function returns every single slope group's dataframe for own purpose.
    return ss_df
