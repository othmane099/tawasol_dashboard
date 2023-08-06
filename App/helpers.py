import calendar
from datetime import datetime
from datetime import timedelta


def sub_hours_from_datetime(datetime_obj, hours_to_sub):
    """
    Subtract a specified number of hours from a given datetime object.

    Parameters:
        datetime_obj (datetime): The original datetime object.
        hours_to_sub (int or float): The number of hours to subtract.

    Returns:
        datetime: The new datetime object after subtracting the specified hours.

    The function takes a datetime object and subtracts the specified number of hours from it.
    It creates a timedelta object with the given number of hours, then subtracts this timedelta
    from the original datetime to obtain the new datetime. The result is returned as a new datetime object.
    """
    # Create a timedelta object representing the specified number of hours to subtract.
    time_delta = timedelta(hours=hours_to_sub)

    # Subtract the time_delta from the datetime_obj to get the new datetime.
    new_datetime = datetime_obj - time_delta

    # Return the new datetime object.
    return new_datetime


def is_datetime_between(datetime_obj, start_datetime, end_datetime):
    """
    Check if a given datetime falls within a specified time range.

    Parameters:
        datetime_obj (datetime): The datetime object to check.
        start_datetime (datetime): The start of the time range.
        end_datetime (datetime): The end of the time range.

    Returns:
        bool: True if the datetime is within the specified time range, False otherwise.

    The function takes a datetime object and checks if it falls within the specified time range,
    which is defined by the start_datetime and end_datetime parameters. The function returns True
    if the datetime is within the range (inclusive), and False otherwise.
    """
    # Check if datetime_obj is between start_datetime and end_datetime (inclusive).
    return start_datetime <= datetime_obj <= end_datetime


def calculate_delta_datetime(start_date_str, end_date_str):
    """
    Calculate the time difference (delta) between two date-time strings.

    Parameters:
        start_date_str (str): A string representing the start date-time.
        end_date_str (str): A string representing the end date-time.

    Returns:
        timedelta: The time difference (delta) between the start and end date-time.

    The function takes two date-time strings and calculates the time difference (delta) between them.
    It first converts the input date-time strings to datetime objects by replacing 'Z' with the timezone offset.
    Then, it calculates the time difference by subtracting the start datetime from the end datetime.
    The result is returned as a timedelta object representing the time difference.
    """
    # Convert the start_date_str to a datetime object and replace 'Z' with timezone offset '+00:00'.
    start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
    # Convert the end_date_str to a datetime object and replace 'Z' with timezone offset '+00:00'.
    end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
    # Calculate the time difference (delta) by subtracting the start datetime from the end datetime.
    response_time = end_date - start_date
    # Return the time difference (delta) as a timedelta object.
    return response_time


def calculate_mean_multiple_delta_datetime(obj_list, start_date, end_date):
    """
    Calculate the mean delta time between start date and end date for a list of objects.

    Parameters:
        obj_list (list): A list of dictionaries, each containing start and end date information.
        start_date (str): The key representing the start date in each dictionary.
        end_date (str): The key representing the end date in each dictionary.

    Returns:
        timedelta: The mean delta time calculated from the list of objects.

    The function takes a list of dictionaries, each containing start and end date information,
    and calculates the delta times between the start and end dates for each object in the list.
    It then calculates the total delta time and divides it by the number of objects to obtain
    the mean delta time, which is returned as a timedelta object.
    """
    # Calculate the delta times between start date and end date for each object in the list.
    delta_times = [calculate_delta_datetime(obj[start_date], obj[end_date]) for obj in obj_list]

    # Calculate the total delta time by summing all the delta times.
    # The initial value for the sum is set to timedelta() to handle an empty list.
    total_delta_time = sum(delta_times, timedelta())

    # Calculate the mean delta time by dividing the total delta time by the number of objects.
    mean_delta_time = total_delta_time / len(delta_times)

    # Return the mean delta time as a timedelta object.
    return mean_delta_time


def format_timedelta(td):
    """
    Format a timedelta object into a dictionary containing days, hours, and minutes.

    Parameters:
        td (timedelta): A timedelta object to be formatted.

    Returns:
        dict: A dictionary containing days, hours, and minutes extracted from the timedelta.

    The dictionary returned will have the following keys:
    - 'days': The number of days in the timedelta.
    - 'hours': The number of hours in the timedelta (excluding days).
    - 'minutes': The number of minutes in the timedelta (excluding days and hours).
    """
    # Extract the number of days from the timedelta.
    days = td.days

    # Convert the total seconds of timedelta to hours and remainder.
    # The remainder is the number of seconds not accounted for in hours.
    hours, remainder = divmod(td.seconds, 3600)

    # Convert the remaining seconds to minutes and seconds.
    minutes, seconds = divmod(remainder, 60)

    # Return a dictionary containing the formatted components of the timedelta.
    return {'days': days, 'hours': hours, 'minutes': minutes}


def sort_by_key(the_list, key='id', desc=True):
    """
    Sort a list of dictionaries based on a specified key.

    Parameters:
        the_list (list): A list of dictionaries to be sorted.
        key (str): The key to be used for sorting. Default is 'id'.
        desc (bool): A boolean flag indicating whether to sort in descending order. Default is True.

    Returns:
        list: The sorted list of dictionaries.

    The function modifies the input list in-place by sorting it based on the specified key.
    It supports sorting in descending or ascending order.
    """
    # Sort the list of dictionaries based on the specified key using lambda function.
    # The 'key' parameter of the 'sort' function defines the sorting criteria.
    # The 'reverse' parameter indicates whether to sort in descending order.
    the_list.sort(key=lambda cl: cl[key], reverse=desc)

    # Return the sorted list of dictionaries.
    return the_list


def calculate_mean_multiple_delta_datetime_formatted(my_list, start_date_key, end_date_key):
    """
    Calculate the mean response time from a list of datetime objects based on the specified keys.

    Parameters:
        my_list (list): A list of dictionaries containing datetime objects.
        start_date_key (str): The key to access the start date in each dictionary.
        end_date_key (str): The key to access the end date in each dictionary.

    Returns:
        str: The formatted mean response time as a string.

    If the input list is empty, the function returns '0:00:00'.
    """
    if my_list:
        # Calculate the mean response time using the provided function.
        mean_response_time = calculate_mean_multiple_delta_datetime(my_list, start_date_key, end_date_key)

        # Format the mean_response_time as a string in 'HH:MM:SS' format.
        formatted_mean_response_time = format_timedelta(mean_response_time)

        # Return the formatted mean response time.
        return formatted_mean_response_time
    else:
        # If the input list is empty, return '0:00:00'.
        return format_timedelta(timedelta())


def group_data_by_month(data_list, date_key):
    """
    Group data from a list of dictionaries by month and count occurrences for each month.

    Parameters:
        data_list (list): A list of dictionaries containing data to be grouped.
        date_key (str): The key representing the date in each dictionary.

    Returns:
        dict: A dictionary containing the count of occurrences for each month.

    The function takes a list of dictionaries and groups them based on the month and year
    extracted from the specified 'date_key'. It then counts the occurrences for each month
    and returns a dictionary with the counts as values and month names as keys.
    """
    current_month = datetime.now().month
    current_year = datetime.now().year

    start_month = 1
    start_year = current_year

    start_date = datetime(start_year, start_month, 1)
    current_date = datetime(current_year, current_month, 1)

    # Generate a list of month and year keys in the format 'Jan 2023'.
    month_year_keys = [m for m in list(calendar.month_name)[1:]]
    month_year_keys = [key[0:3] for key in month_year_keys if
                       start_date <= datetime.strptime(f"{key} {current_year}", "%B %Y") <= current_date]

    # Create a dictionary with month and year keys and initial count as 0 for each month.
    date_list = {key: 0 for key in month_year_keys}

    for obj in data_list:
        date_str = obj[date_key]

        # Parse the date string into a datetime object.
        date_obj = parse_string_datetime(date_str)

        # Get the month and year key for the current date object.
        month_year_key = list(date_list.keys())[date_obj.month - 1]

        # Increment the count for the corresponding month in the dictionary.
        if month_year_key in date_list:
            date_list[month_year_key] += 1

    # Return the dictionary with counts for each month.
    return date_list


def parse_string_datetime(date_str):
    """
    Parse a string representing a datetime in the specified formats.

    Parameters:
        date_str (str): A string representing a datetime.

    Returns:
        datetime: A datetime object parsed from the input string.

    The function tries to parse the input string into a datetime object using two formats:
    - '%Y-%m-%dT%H:%M:%SZ' (e.g., '2023-08-03T12:34:56Z')
    - '%Y-%m-%dT%H:%M:%S.%fZ' (e.g., '2023-08-03T12:34:56.789Z')

    If the input string does not match any of the formats, a ValueError is raised.
    """
    try:
        # Try parsing the date string using the format '%Y-%m-%dT%H:%M:%SZ'.
        date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        try:
            # If the first format fails, try parsing using the format '%Y-%m-%dT%H:%M:%S.%fZ'.
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            # If both formats fail, raise a ValueError with an error message.
            raise ValueError("Invalid date format")

    # Return the parsed datetime object.
    return date_obj


def format_percentage(number):
    """
    Format a decimal number by removing the decimal part if it equals 0, otherwise, it takes 2 numbers from the
    decimal part.

    Parameters:
        number (float): Any number to be formatted.

    Returns:
        str: The formatted number as a string.

    The function takes a decimal number and formats it by removing the decimal part if it equals 0,
    or it keeps 2 numbers from the decimal part if they are non-zero. The resulting number is returned as a string.
    """
    # Format the number with 2 decimal places using the "{:.2f}" format specifier.
    formatted_number = "{:.2f}".format(number)

    # Remove trailing zeros from the right side of the formatted number.
    formatted_number = formatted_number.rstrip("0")

    # If the number ends with '.', remove it as well.
    formatted_number = formatted_number.rstrip(".")

    # Return the formatted number as a string.
    return formatted_number
