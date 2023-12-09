import pandas as pd
import numpy as np


def preprocess(df, holidays, schools, weather):
    '''
    Preprocesses the data by adding date based features, holiday features and weather features.
    '''
    print('Starting preprocessing, adding date based features...')
    
    #add date based features
    df['Day'] = pd.to_datetime(df['Date'], utc=True).dt.date
    df['Weekday'] = pd.to_datetime(df['Date'], utc=True).dt.weekday
    df['Month'] = pd.to_datetime(df['Date'], utc=True).dt.month
    df['Year'] = pd.to_datetime(df['Date'], utc=True).dt.year
    
    #add boolean for weekend
    df['Weekend'] = 0
    df.loc[df['Weekday'] == 5, 'Weekend'] = 1
    df.loc[df['Weekday'] == 6, 'Weekend'] = 1
    
    #add season
    df['Season'] = None
    df.loc[df['Month'] == 1, 'Season'] = 'Winter'
    df.loc[df['Month'] == 2, 'Season'] = 'Winter'
    df.loc[df['Month'] == 3, 'Season'] = 'Spring'
    df.loc[df['Month'] == 4, 'Season'] = 'Spring'
    df.loc[df['Month'] == 5, 'Season'] = 'Spring'
    df.loc[df['Month'] == 6, 'Season'] = 'Summer'
    df.loc[df['Month'] == 7, 'Season'] = 'Summer'
    df.loc[df['Month'] == 8, 'Season'] = 'Summer'
    df.loc[df['Month'] == 9, 'Season'] = 'Autumn'
    df.loc[df['Month'] == 10, 'Season'] = 'Autumn'
    df.loc[df['Month'] == 11, 'Season'] = 'Autumn'
    df.loc[df['Month'] == 12, 'Season'] = 'Winter'
    
    print('Adding holiday features...')
    
    #add public holidays and school holidays
    df['Holiday'] = None
    for i in range(len(holidays)):
        df.loc[df['Day'] == holidays['Date'][i], 'Holiday'] = holidays['Holiday'][i]
        
    df['SchoolHoliday'] = None
    for i in range(len(schools)):
        df.loc[df['Day'] == schools['Date'][i], 'SchoolHoliday'] = schools['Holiday'][i]
        
    #add boolean for holiday
    df['HolidayBool'] = 0
    df.loc[df['Holiday'].notnull(), 'HolidayBool'] = 1
    df.loc[df['SchoolHoliday'].notnull(), 'HolidayBool'] = 1
    
    print('Adding weather features...')
    
    #add weather features
    df = df.merge(weather, how='left', left_on='Day', right_on='Date')
    df.drop(['Date_y', 'Station_code'], axis=1, inplace=True)
    df.rename(columns={'Date_x': 'Date'}, inplace=True)

    #add boolean for rain
    df['RainBool'] = 0
    df.loc[df['Rain'] > 0, 'RainBool'] = 1
    
    return df