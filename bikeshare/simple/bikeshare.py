import calendar
import os
import time

import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

DIRECTORY = '.'


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function '{func.__name__}' took {execution_time:.4f} seconds to execute.")
        return result

    return wrapper


def list_sources(dir):
    city_names = [filename.replace('.csv', '').replace('_', ' ') for filename in os.listdir(dir) if
                  filename.endswith('.csv')]

    csv_files = [filename for filename in os.listdir(dir) if filename.endswith('.csv')]

    return {k: v for k, v in zip(city_names, csv_files)}


def choice_enum_iteration(**kwargs):
    select_statement = ""
    while True:

        if 'selectall' in kwargs:
            select_statement = (f", '{kwargs['selectall']}' for all select ")

        for index, choice in enumerate(kwargs['calclist'], start=1):
            print(f"{index}. {choice}")

        first_index = 1
        last_index = len(kwargs['calclist'])

        user_choice = input(
            f"\nSelect a {kwargs['name']} by entering the corresponding number ({first_index}-{last_index}){select_statement} or '{kwargs['exitchar']}' for exit: \n")

        if user_choice.lower() == kwargs['exitchar']:
            print("OK Bye...")
            exit(0)

        if 'selectall' in kwargs and user_choice.lower() == kwargs['selectall']:
            selection = None
            print(f"You have chosen to select all the {kwargs['name']}\n")
            break

        if user_choice.isdigit():
            choice = int(user_choice)
            if first_index <= choice <= last_index:
                selection = kwargs['calclist'][choice - 1]
                print('=' * 80)
                print(f"You selected: {selection}")
                print('=' * 80)
                break
            else:
                print('=' * 80)
                print(
                    f"Invalid choice. Please enter a number between ({first_index}-{last_index}){select_statement} or '{kwargs['exitchar']}' for exit: ")
                print('=' * 80)

        else:
            print('\n=' * 80)
            print(
                f"Invalid input. Please enter a number between ({first_index}-{last_index}){select_statement} or '{kwargs['exitchar']}' for exit: ")
            print('=' * 80)

    return selection


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("\nHello! Let's explore some US bikeshare data!\n")

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_csv_source = list_sources(DIRECTORY)

    cities = list(city_csv_source.keys())

    print("\nHere are the available cities with a valid csv:\n")

    city_choice = choice_enum_iteration(name='city details', calclist=cities, exitchar='x', selectall='a')

    city = next(({key: value} for key, value in city_csv_source.items() if key == city_choice), city_csv_source)

    # get user input for month (all, january, february, ... , june)

    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    month = choice_enum_iteration(name='month', calclist=months, exitchar='x', selectall='a')

    # get user input for day of week (all, monday, tuesday, ... sunday)

    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    day = choice_enum_iteration(name='day', calclist=days_of_week, exitchar='x', selectall='a')

    return {"city": city, "month": month, "day": day}


@timing_decorator
def load_data(**kwargs):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df_combined = pd.DataFrame()
    df = None
    raw_dict = {
        'month_key': kwargs["month"],
        'day_of_week_key': kwargs["day"],
    }

    for city, filename in kwargs['city'].items():
        try:
            df = pd.read_csv(f'{DIRECTORY}/{filename}')
            if not df.empty:
                df['city'] = city
                df_combined = pd.concat(
                    [df_combined, df])  # Concatenate the non-empty DataFrame to the combined DataFrame
                print(f"City: {city}")
                print(df)
            else:
                print(f"Warning: CSV file '{filename}' is empty or has no columns.")
        except FileNotFoundError:
            print(f"Error: CSV file '{filename}' not found.")
        except pd.errors.EmptyDataError:
            print(f"Warning: CSV file '{filename}' is empty.")
        except Exception as e:
            print(f"Error: An exception occurred while reading CSV file '{filename}': {str(e)}")

    if not df_combined.empty:
        df_combined['Start Time'] = pd.to_datetime(df_combined['Start Time'])

        filtered_data = df_combined.copy()

        for key, value in raw_dict.items():
            if value is not None:
                if key == 'month_key':
                    filtered_data = filtered_data[filtered_data['Start Time'].dt.strftime('%B') == value]
                elif key == 'day_of_week_key':
                    filtered_data = filtered_data[filtered_data['Start Time'].dt.strftime('%A') == value]

        df = filtered_data

    return df


@timing_decorator
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')

    # display the most common month

    # display the most common day of week

    # display the most common start hour

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    choices = ['most common month', 'most common day of week', 'most common start hour']

    choice = choice_enum_iteration(name='choices', calclist=choices, exitchar='x')

    if choice == 'most common month':
        df['month'] = df['Start Time'].dt.month
        month_counts = df['month'].value_counts()
        most_common_month = month_counts.index[0]
        month_name = calendar.month_name[most_common_month]
        print("\nMost common month:", month_name)

    elif choice == 'most common day of week':
        df['day_of_week'] = df['Start Time'].dt.day_name()
        day_counts = df['day_of_week'].value_counts()
        most_common_day = day_counts.index[0]
        print("\nMost common day of the week:", most_common_day)

    elif choice == 'most common start hour':
        df['start_hour'] = df['Start Time'].dt.hour
        hour_counts = df['start_hour'].value_counts()
        most_common_hour = hour_counts.index[0]
        print("\nMost common start hour:", most_common_hour)

    else:
        print("\nWrong Choice!")


@timing_decorator
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')

    # display most commonly used start station

    # display most commonly used end station

    # display most frequent combination of start station and end station trip

    choices = ['most commonly used start station', 'most commonly used end station',
               'most frequent combination of start station and end station trip']

    choice = choice_enum_iteration(name='choices', calclist=choices, exitchar='x')

    if choice == 'most commonly used start station':
        station_counts = df['Start Station'].value_counts()
        most_common_start_station = station_counts.index[0]
        print("\nMost commonly used start station:", most_common_start_station)

    elif choice == 'most commonly used end station':
        station_counts = df['End Station'].value_counts()
        most_common_end_station = station_counts.index[0]
        print("\nMost commonly used end station:", most_common_end_station)

    elif choice == 'most frequent combination of start station and end station trip':
        station_combinations = df.groupby(['Start Station', 'End Station']).size()
        most_frequent_combination = station_combinations.idxmax()
        print("\nMost frequent combination of start station and end station trip:", most_frequent_combination)

    else:
        print("Wrong Choice!")

    print('=' * 40)


@timing_decorator
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')

    # display total travel time

    # display mean travel time

    choices = ['total travel time', 'mean travel time']

    choice = choice_enum_iteration(name='choices', calclist=choices, exitchar='x')

    if choice == 'total travel time':
        total_travel_time = df['Trip Duration'].sum()
        print("\nTotal travel time:", total_travel_time)

    elif choice == 'mean travel time':
        mean_travel_time = df['Trip Duration'].mean()
        print("\nMean travel time:", mean_travel_time)

    else:
        print("Wrong Choice!")

    print('=' * 40)


@timing_decorator
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')

    # Display counts of user types

    # Display counts of gender

    # Display earliest, most recent, and most common year of birth

    # print("\nThis took %s seconds." % (time.time() - start_time))

    choices = ['counts of user types', 'counts of gender', 'earliest, most recent, and most common year of birth']

    choice = choice_enum_iteration(name='choices', calclist=choices, exitchar='x')

    if choice == 'counts of user types':
        user_type_counts = df['User Type'].value_counts()
        print("\nCounts of user types:", user_type_counts)

    elif choice == 'counts of gender':
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of gender :", gender_counts)


    elif choice == 'earliest, most recent, and most common year of birth':
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode().values[0]
        print("\nEarliest year of birth:", earliest_year)
        print("\nMost recent year of birth:", most_recent_year)
        print("\nMost common year of birth:", most_common_year)


    else:
        print("Wrong Choice!")

    print('=' * 40)


def main():
    while True:
        filters = get_filters()

        df = load_data(**filters)

        if df is None or df.empty:
            print('=' * 80)
            print("DataFrame is either None or empty.")
            print('=' * 80)
            continue
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        restart = input('\nWould you like to restart? Enter y or n.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()
