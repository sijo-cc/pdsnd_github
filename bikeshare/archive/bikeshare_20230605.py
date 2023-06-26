import os
import time
import pandas as pd


def command():
    return DivyBikeShareCalc()


class DivyBikeShareCalc():

    # CITY_DATA = {'chicago': 'chicago.csv',
    #              'new york city': 'new_york_city.csv',
    #              'washington': 'washington.csv'}

    DIRECTORY = 'source'

    def timing_decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Function '{func.__name__}' took {execution_time:.4f} seconds to execute.")
            return result
        return wrapper

    def __init__(self):

        print("\n=====  Welcome to the bikeshare interactive csv analysis interface  ======\n")

        find_city_sources = self.list_sources(self.DIRECTORY)

        print(find_city_sources)

        city_csv_to_process = self.csv_to_process(find_city_sources)

        print(city_csv_to_process)

        month, day = self.get_filters()

        print(city_csv_to_process, find_city_sources[city_csv_to_process],month,day)

        df = self.load_data(city_csv_to_process, find_city_sources[city_csv_to_process],month,day)

        # while True:
        #     city, month, day = self.get_filters()
        #     df = self.load_data(city, month, day)
        #
        #     self.time_stats(df)
        #     self.station_stats(df)
        #     self.trip_duration_stats(df)
        #     self.user_stats(df)
        #
        #     restart = input('\nWould you like to restart? Enter y or n.\n')
        #     if restart.lower() != 'y':
        #         break

    def enum_iteration(self, **kwargs):

        for index, choice in enumerate(kwargs['calclist'], start=1):
            print(f"{index}. {choice}")

        first_index = 1
        last_index = len(kwargs['calclist'])

        while True:
            user_choice = input(f"\nSelect a {kwargs['name']} by entering the corresponding number ({first_index}-{last_index}): ")

            if user_choice.lower() == kwargs['exitchar']:
                print("OK Bye...")
                exit(0)

            if user_choice.isdigit():
                choice = int(user_choice)
                if first_index <= choice <= last_index:
                    selection = kwargs['calclist'][choice - 1]
                    print("You selected:", selection)
                    break
                else:
                    print(f"Invalid choice. Please enter a number between {first_index} and {last_index}.")
                    print('-' * 40)
            else:
                print("Invalid input. Please enter a number.")
                print('-' * 40)

        return selection

    def csv_to_process(self, city_data):

        keys_list = list(city_data.keys())

        print("\nHere are the available cities with a valid csv:\n")

        city = self.enum_iteration(name='city details', calclist=keys_list, exitchar='x')

        # while True:
        #     print('-' * 20)
        #     for index, item in enumerate(keys_list):
        #         print(index, item)
        #     print('-' * 20)
        #
        #     user_input = input("Enter a number choice , corresponding to the city (type 'x' to exit): ")
        #     print('\n')
        #
        #
        #     if user_input.lower() == 'x':
        #         print("OK Bye...")
        #         break
        #
        #     if user_input.isdigit():
        #         index = int(user_input)
        #         if 0 <= index < len(keys_list):
        #             key = keys_list[index]
        #             value = city_data[key]
        #             print(f'You have chosen city: "{key}" and the source for this is "{value}" \n')
        #             break
        #         else:
        #             print("Invalid choice. Please try again (type 'x' to exit).\n")
        #     else:
        #         print("Invalid input! Please choose a number (type 'x' to exit).\n")

        return city

    def list_sources(self, dir):

        city_names = [filename.replace('.csv', '').replace('_', ' ') for filename in os.listdir(dir) if
                      filename.endswith('.csv')]

        csv_files = [filename for filename in os.listdir(dir) if filename.endswith('.csv')]

        return {k: v for k, v in zip(city_names, csv_files)}


    def get_filters(self):



        """
        Asks user to specify a month, and day to analyze.
    
        Returns:
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
        """
        print('Hello! Let\'s explore some US bikeshare data!')

        # get user input for month (all, january, february, ... , june)



        # get user input for day of week (all, monday, tuesday, ... sunday)




        # for index, month in enumerate(months, start=1):
        #     print(f"{index}. {month}")
        #
        # while True:
        #     user_choice = input("\nSelect a month by entering the corresponding number (1-12): ")
        #
        #     if user_choice.isdigit():
        #         choice = int(user_choice)
        #         if 1 <= choice <= 12:
        #             selected_month = months[choice - 1]
        #             print("You selected:", selected_month)
        #             break
        #         else:
        #             print("Invalid choice. Please enter a number between 1 and 12.")
        #     else:
        #         print("Invalid input. Please enter a number.")


        #
        # for index, day in enumerate(days_of_week, start=1):
        #     print(f"{index}. {day}")
        #
        # while True:
        #     user_choice = input("Select a day by entering the corresponding number (1-7): ")
        #
        #     if user_choice.isdigit():
        #         choice = int(user_choice)
        #         if 1 <= choice <= 7:
        #             selected_day = days_of_week[choice - 1]
        #             print("You selected:", selected_day)
        #             break
        #         else:
        #             print("Invalid choice. Please enter a number between 1 and 7.")
        #     else:
        #         print("Invalid input. Please enter a number.")
        # print('-' * 40)

        print("Hello! Let's explore some US bikeshare data! \n")

        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        month = self.enum_iteration(name='month',calclist=months,exitchar='x' )
        day = self.enum_iteration(name='day', calclist=days_of_week, exitchar='x')


        return month, day

    def load_data(self, city, csv, month, day):
        df = []
        try:
            df = pd.read_csv(f'{self.DIRECTORY}/{csv}')

        except Exception as e:
            print(f'Exception while trying to read the data source: {e}\n')




        """
        Loads data for the specified city and filters by month and day if applicable.
    
        Args:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
        Returns:
            df - Pandas DataFrame containing city data filtered by month and day
        """

        return df

    @timing_decorator
    def time_stats(self, df):
        """Displays statistics on the most frequent times of travel."""

        print('\nCalculating The Most Frequent Times of Travel...\n')
        # start_time = time.time()

        # display the most common month

        # display the most common day of week

        # display the most common start hour

        # print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)

    @timing_decorator
    def station_stats(self, df):
        """Displays statistics on the most popular stations and trip."""

        print('\nCalculating The Most Popular Stations and Trip...\n')
        # start_time = time.time()

        # display most commonly used start station

        # display most commonly used end station

        # display most frequent combination of start station and end station trip

        # print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)

    @timing_decorator
    def trip_duration_stats(self, df):
        """Displays statistics on the total and average trip duration."""

        print('\nCalculating Trip Duration...\n')
        # start_time = time.time()

        # display total travel time

        # display mean travel time

        # print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)

    @timing_decorator
    def user_stats(self, df):
        """Displays statistics on bikeshare users."""

        print('\nCalculating User Stats...\n')
        # start_time = time.time()

        # Display counts of user types

        # Display counts of gender

        # Display earliest, most recent, and most common year of birth

        # print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)

