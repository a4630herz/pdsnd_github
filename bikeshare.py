import time
import pandas as pd
import numpy as np

pd.set_option("display.max_rows", None, "display.max_columns", None)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

list_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
list_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    # define default parameters which are empty strings
    city, filter, month, day = "", "", "", ""

    # get user input for city (chicago, new york city, washington).
    while city not in CITY_DATA.keys():
        city = input('Would you like to see data for Chicago, New York, or Washington? ').lower()

    while filter not in ['month', 'day', 'both', 'none']:
        filter = input('Would you like to filter the data by month, day, both or not at all?\nType \"none\" for no time filter.\n').lower()

    # get user input for month (all, january, february, ... , june)
    if filter in ['month', 'both']:
        while month not in list_months:
            month = input('Which month would you like to explore -\nJanuary, February, March, April, May, or June?\nType \"all\" for no month filter.\n').lower()
    else:
        month = "all"

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter in ['day', 'both']:
        while day not in list_days:
            day = input('Which day would you like to explore -\nMonday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\nType \"all\" for no day filter.\n').lower()
    else:
        day = "all"

    print("\n"+city)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA.get(city))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month_int = list_months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df["month"] == month_int]


    # filter by weekday if applicable
    if day != 'all':
        # filter by weekday to create the new dataframe
        day_int = list_days.index(day)

        df = df[df["weekday"] == day_int]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    count_max = df.groupby(['month']).count().max()[0]
    print("   The most popular month is {} with {} counts.".format(list_months[popular_month-1], count_max))

    # display the most common day of week
    popular_day_of_week = df['weekday'].mode()[0]
    count_max = df.groupby(['weekday']).count().max()[0]
    print("   The most popular day of the week is {} with {} counts.".format(list_days[popular_day_of_week], count_max))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    count_max = df.groupby(['hour']).count().max()[0]
    if 12 <= popular_hour <= 23:
        half = 'pm'
    else:
        half = 'am'
    if popular_hour >= 13:
        hour_half = popular_hour - 12
    else:
        hour_half = popular_hour
    print("   The most popular start hour is {}{} with {} counts.".format(hour_half, half, count_max))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    count_max = df.groupby(['Start Station']).count().max()[0]
    print("   The most popular start station is {} with {} counts.".format(popular_start_station, count_max))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    count_max = df.groupby(['End Station']).count().max()[0]
    print("   The most popular end station is {} with {} counts.".format(popular_end_station, count_max))

    # display most frequent combination of start station and end station trip
    df_se = df[['Start Station', 'End Station']]
    count_max = df.groupby(['Start Station', 'End Station']).count().max()[0]
    print("   The most popular combination of start and end station is {} (start) - {} (end) with {} counts."\
          .format(df_se.mode()['Start Station'][0], df_se.mode()['End Station'][0], count_max))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    time_travel_sum = df["Trip Duration"].sum()
    print("   The total travel time is {} seconds.".format(time_travel_sum))

    # display mean travel time
    time_travel_mean = df["Trip Duration"].mean()
    print("   The mean travel time is {} seconds, which is {} minutes.".format(time_travel_mean, time_travel_mean/60.))

    # display min and max travel time
    time_travel_max = df["Trip Duration"].max()
    time_travel_min = df["Trip Duration"].min()
    print("   The shortest travel time is {} minutes, the longest travel time is {} minutes.".format(time_travel_min/60., time_travel_max/60.))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    df_user = df.groupby(['User Type']).count()['Start Time']
    print('   Showing user types:')
    for index, value in df_user.items():
        print("      {}: {} counts".format(index, value))


    # Display counts of gender
    df_user = df.groupby(['Gender']).count()['Start Time']
    print('   Showing genders:')
    for index, value in df_user.items():
        print("      {}: {} counts".format(index, value))

    # Display earliest, most recent, and most common year of birth
    birth_latest = df["Birth Year"].max()
    birth_earliest = df["Birth Year"].min()
    birth_common = df['Birth Year'].mode()[0]
    count_max = df.groupby(['Birth Year']).count().max()[0]
    print("   Showing birth year:")
    print("      The earliest birth year is {}, the latest birth year is {}.".format(int(birth_earliest), int(birth_latest)))
    print("      The most common birth year is {} with {} counts.".format(int(birth_common), count_max))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays raw data of data frame, 5 rows each time before asking whether to continue"""
    counter = 0
    wanna_see = input("Do you want to see raw data? Please answer yes or no. ").lower()
    #df_raw = df.drop(['month', 'weekday', 'hour'], axis = 1).copy()
    size_df = df.shape[0]
    while (wanna_see == "yes" and counter + 5 <= size_df):
        print(df.iloc[counter:counter+5, 0:-3])
        wanna_see = input("Do you want to see more raw data? Please answer yes or no. ").lower()
        counter += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        if city in ['new york', 'chicago']:
            user_stats(df)
        elif city == "washington":
            print("\nSorry, there is no user data available for {}!\n\n{}\n".format(city.title(), '-'*40))
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
