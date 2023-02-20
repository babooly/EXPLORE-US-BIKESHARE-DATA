"""
@author: eslam
"""
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    #user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs)
    city = input('which city would you like to choose: chicago, new york city, washington \n').lower()
    while city not in CITY_DATA.keys():
        print('invalid inputs, please choose a city from: chicago, new york city, washington \n')
        city = input('which city would you like to choose: chicago, new york city, washington \n').lower()

    #user input for month (all, january, february, ... , june)
    def the_month_filter():
         months = {"1": "january", "2": 'february', '3': 'march','4': 'april', '5': 'may', '6': 'june'}
         month = input('please choose the month: (1)january, (2)february, (3)march, (4)april, (5)may, (6)june\n').lower()
         while month not in (list(months.values())+list(months.keys())):
                print('please choose a month from: january, february, march, april, may, june')
                month = input('please choose the month: (1)january, (2)february, (3)march, (4)april, (5)may, (6)june\n').lower()
                continue    
         if month in list(months.keys()):
            month = months[month]
         return month
                
    #user input for day of week (all, monday, tuesday, ... sunday)
    def the_day_filter():
        
        days = {'1': 'sunday', '2': 'monday', '3': 'tuesday', '4': 'wednesday', '5': 'thursday', '6': 'friday', '7': 'saturday'}
        day = input('please choose the day: (1)sunday, (2)monday, (3)tuesday, (4)wednesday, (5)thursday, (6)friday, (7)saturday \n').lower()
        while day not in (list(days.values())+list(days.keys())):
            print('invalid inputs, please choose the day: (1)sunday, (2)monday, (3)tuesday, (4)wednesday, (5)thursday, (6)friday, (7)saturday \n')
            day = input('please choose the day: (1)sunday, (2)monday, (3)tuesday, (4)wednesday, (5)thursday, (6)friday, (7)saturday \n').lower()
            continue
        if day in list(days.keys()):
            day = days[day]
        return day
    
    #the filter to analyze the time        
    filtering = ['month','day','both','none']
    tf = input('filter by : month, day, both, none\n')
    while tf not in filtering:
        print("please choose a filter : month, day, both, none\n")
        tf = input('filter by : month, day, both, none\n')
    
    if tf in ('both'):
        month = the_month_filter()
        day = the_day_filter()
        
    elif tf in ('month'):
        month = the_month_filter()
        day = 'all' 
    
    elif tf in ('day'):
        day = the_day_filter()
        month = 'all'
        
    elif tf in ('none'):
        month = 'all'
        day = 'all'
    print('-'*40)
    return city, month, day

 

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    df["day_of_week"] = df['Start Time'].dt.day_name()
    df["month"] = df['Start Time'].dt.month
    #filter by day of week
    if month != 'all':
        
        #filter by month to create the new dataframe
        month_list = ["january", 'february', 'march', 'april', 'may', 'june']
        month = month_list.index(month)+1
        df = df[df['month'] == month]
        
    if day != 'all':
        
        #filter by day to create new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df




def time_stats(df):
    """The function of the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # the most common month
    month_list = ["January", 'February', 'March', 'April', 'May', 'June']
    month = month_list[(df['month'].mode()[0])-1]
    print(f"Most Common Start Month: {month}")

    #the most common day of week
    print(f"Most Common Start Day Of Week: {df['day_of_week'].mode()[0]}")

    # the most common start hour
    print(f"Most Common Start Hour: {(df['hour'].mode()[0])}")

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

 


def station_stats(df):
    """The function of the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #most commonly used start station
    print(f"Most Common Start Station: {df['Start Station'].mode()[0]}")

    #most commonly used end station
    print(f"Most Common End Station: {df['End Station'].mode()[0]}")

    #most frequent combination of start station and end station trip
    df['route'] = df['Start Station']+","+df['End Station']
    print(f"the most common route: \n  {df['route'].mode()[0]}")
 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    


def trip_duration_stats(df):
    """The function of the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    total_time = df['Trip Duration'].sum()
    print("total travel time:",round(total_time), 'seconds or ', round(total_time)/3600, 'hours')

    #display mean travel time
    average_time = df['Trip Duration'].mean()
    print("average travel time:",round(average_time), 'seconds or ', round(average_time)/3600, 'hours')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def user_stats(df):
    """The function of the bikeshare users."""
    
    start_time = time.time()
    #counts of user types
    print(df['User Type'].value_counts().to_frame())
    
    #counts of gender
    if 'Gender' in df.columns:
        print(df['Gender'].value_counts().to_frame())
    
    #earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\n earliest, most recent, and most common year of birth\n')
        print(f"The earliest year of birth: {int(df['Birth Year'].min())}")
        
        print(f"The most recent year of birth: {int(df['Birth Year'].max())}")
     
        print(f"The most common year of birth: {int(df['Birth Year'].mode()[0])}")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """
    The function of the first 5 rows and if you wants the next 5 rows ?
    """
    row = 0 
    a = input('would you like to see the frist five rows: yes, no\n').lower()
    while True:
        if a == ('yes'):
            pd.set_option('display.max_columns',None)
            print(df.iloc[row:row+5])
            a = input('would you like to see the frist five rows: yes, no\n').lower()
            row += 5
            continue
        elif a == ('no'):
            break 
        else:
            print('invalid inputs')
            a = input('next 5 rows ?\n').lower()
            continue 
        
        
def main():
    """
    The main function which Asks the user if he wants to restart or no ?
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
