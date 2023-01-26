import time
import math
import statistics
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    city = input('Write your choosen city from this options:[chicago, new york city, washington]\n :-').lower()
    while city not in CITY_DATA.keys():
        print('Enter Valid City')
        city = input('Write your choosen city from this options:[chicago, new york city, washington]\n :-').lower()
        print('You enterd: {}.\n'.format(city))
        break

    # get user input for month (all, january, february, ... , june)
    months = ['january','february','march' ,'april' ,'may' ,'june','all']
    while True:
        month = input('Write your choised month without\'\':{}\n'.format(months)).lower()
        if month in months:
            break
        else:
            print('Enter Valid Month')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    week_days = ['monday','tuesday','wednesday','thursday', 'friday','saturday','sunday','all']
    while True:
        day = input('Write your choised day without\'\':{}\n'.format(week_days)).lower()
        if day in week_days:
            break
        else:
            print('Enter Valid Day')

    print('-'*40)
    print("You Enterd {} {} {}", city, month, day) 
    return city, month, day

def load_data(city,month,day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load the data file related to the sekected city into a dataframe df
    df=pd.read_csv(CITY_DATA[city])
    # convert the Start Time column datatype to datetime
    df['Start Time']=pd.to_datetime(df['Start Time'])
    # get month, day of week and Hour from Start Time column to three new added columns
    df['month']=df['Start Time'].dt.month
    df['weak_day'] = df['Start Time'].dt.day_name()  # correction error(1) 
    df['start_hour']=df['Start Time'].dt.hour
    if month != 'all':
        months = ['january','february','march' ,'april' ,'may' ,'june']
        month = months.index(month)+1
        df = df[df['month'] == month]
    if 'day' != 'all':
        
        df = df[df['weak_day'] == day.title()]
        
    # Ask user to display summary Description of data
    ask_Descrip_stat=""
    while ask_Descrip_stat !='yes' and ask_Descrip_stat!='no':
        ask_Descrip_stat=input('Do you need to see summary Description of data? Enter yes or no').lower()
    
    if ask_Descrip_stat =='yes':
        print (df.describe(include='all'))
    else:
        print('Ok, you need only calculation  about your filtred data')
           
    return df
    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    most_repeating_month=df['month'].mode()
    print('the most common month is {}'.format(most_repeating_month))
    # display the most common day of week
    most_repeating_day=df['weak_day'].mode()
    print('the most common day is {}'.format(most_repeating_day))
    # display the most common start hour
    most_repetaing_start_hour=df['start_hour'].mode()
    print('the most common start hour is {}'.format(most_repetaing_start_hour))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('the most commonly used start station is {}'.format(df['Start Station'].mode()))

    # display most commonly used end station
    print('the most commonly used end station is {}'.format(df['End Station'].mode()))

    # display most frequent combination of start station and end station trip

    df['route']=df['Start Station']+ "," + df['End Station']
    print('the most common trip ie: route is {}'.format(df['route'].mode()))

    print("\n This took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('total travel time :', df['Trip Duration'].sum().round())
    
    # display mean travel time
    print('average travel time :', df['Trip Duration'].mean())

    print("\n This took %s seconds." % (time.time() - start_time))          
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    
    print(df['User Type'].value_counts())
    # Display counts of gender
    # I've been correcting error 2 
    if city != 'washington':
        print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    # print('the most commonly used end station is {}'.format(df['End Station'].mode()))

        print('The most common year of birth is {}' .format(df['Birth Year'].mode()))
        print('The most recent year of birth is {}' .format(df['Birth Year'].max()))
        print('The most earliest year of birth is {}'.format(df['Birth Year'].min()))
    else:
        print(' This city has \"No Related Data\" to explore !') 

    print("\n This took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def sample_Raw_data_dispaly(df):
    row_num =0
    while row_num <5 :
 
        display = input('\n Would you like to to see data sample? Enter yes or no.\n').lower()
        if display == "yes":
            
            print(df.iloc[row_num: row_num + 5])
            row_num += 5
            
        elif display == "no":
            break
        else: #validate user input
            print("Sorry!.. Wrong Input!,")

def main():
    while True:
        city,month,day = get_filters()
        df = load_data(city,month,day)
        print(">>>>>> ", df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        sample_Raw_data_dispaly(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Thank for Exloring \"US BikeShare Data\"')
            break


if __name__ == "__main__":
    main()