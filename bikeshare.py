import time
import pandas as pd
import numpy as np

# creating dictionary to relate city name to its csv file
CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}

# creating list container for values of city, month and day of weeks
city_list = ["chicago", "new york city", "washington"]
month_list = ["january", "February", "march", "april", "may", "june", "july", "august", "september", "october",
              "november", "december", "all"]
day_list = ["saturday", "sunday", "monday", "tuesday", "wednesday", "tuesday", "friday", "all"]


# creating a function to evaluate to input inserted by user for city name is valid or not
def city_true(city_str):
    while True:
        city_input = input(city_str).lower()
        try:
            if city_input in city_list:
                break
            else:
                print("wrong spelling of city name")
        except ValueError:
            print("this is not a city")
    return city_input


# creating a function to evaluate to input inserted by user for month name is valid or not
def month_true(month_str):
    while True:
        month_input = input(month_str).lower()
        try:
            if month_input in month_list:
                break
            else:
                print("wrong spelling of month name")
        except ValueError:
            print("this is not a month")
    return month_input


# creating a function to evaluate to input inserted by user for day name is valid or not
def day_true(day_str):
    while True:
        day_input = input(day_str).lower()
        try:
            if day_input in day_list:
                break
            else:
                print("wrong spelling of day name")
        except ValueError:
            print("this is not a day")
    return day_input


# creating a function to define the filter and to allow user to know the good spelling of inputs
def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    city = city_true("select one of the following cities : chicago, new york city, washington:\n")
    month = month_true("select the month you need to query about like january, february, march, april, may, june,"
                       " july, august, september, october, november, december or all:\n")
    day = day_true("select the day you need to query about like saturday, sunday, ,monday, tuesday, wednesday, thursday,"
                   " friday or all:\n")
    """
        Asks user to specify a city, month, and day to analyze.

        Returns:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
        """

    # get user input for month (all, january, february, ... , june)

    # get user input for day of week (all, monday, tuesday, ... sunday)

    print('-'*100)
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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month = month_list.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month

    # display the most common day of week

    # display the most common start hour

    common_month = df['month'].mode()[0]
    print('Most common Month:', common_month)

    common_week_day = df['day_of_week'].mode()[0]
    print('common Day Of Week:', common_week_day)

    common_start_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    # display most commonly used end station

    # display most frequent combination of start station and end station trip

    common_start_station = df['Start Station'].mode()[0]
    print('most commonly used start station:\n ', common_start_station)

    common_end_station = df['End Station'].mode()[0]
    print('most commonly used end station:\n ', common_end_station)

    end_start = df.groupby(['Start Station', 'End Station'])
    frequent_combination = end_start.size().sort_values(ascending=False).head(1)
    print('most frequent combination of start station and end station trip:\n', frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    # display mean travel time

    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)

    avg_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', avg_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 100)


def user_stats(df, city):
    # Display counts of user types

    # Display counts of gender

    # Display earliest, most recent, and most common year of birth

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_tcount = df['User Type'].value_counts()
    print("counts of user types:\n ", user_tcount)

    if city != 'washington':
        gender_stat = df['Gender'].value_counts()
        print("counts of gender:\n ", gender_stat)

        earliest_year = df['Birth Year'].min()
        print('Earliest Year:', earliest_year)

        recent_year = df['Birth Year'].max()
        print('Most Recent Year:', recent_year)

        common_year = df['Birth Year'].mode()[0]
        print('Most Common Year of birth:', common_year)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 80)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print(df.head())

        iterate_more = input("if you need to see the next five row say yes otherwise say no:\n")
        while iterate_more.lower() == "yes":
            try:
                for chunk in pd.read_csv(CITY_DATA[city], index_col=0, chunksize=5):
                    print(chunk)
                    iterate_more = input("if you need to see the next five row say yes otherwise say no:\n")
                    if iterate_more.lower() != 'yes':
                        print('Thank You')
                        break
            except KeyboardInterrupt:
                print('Thank you.')

            break

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()