from datetime import datetime

from App import repositories, constants
from App.forms import ConfigForm
from App.helpers import sort_by_key, sub_hours_from_datetime, \
    is_datetime_between, calculate_mean_multiple_delta_datetime_formatted, format_percentage, group_data_by_month
from App.repositories import get_configuration, create_configuration, update_configuration


def dashboard_fake_data():
    started_claims = [{'publish_date': "2023-07-01T11:26:00.210087Z", "start_date": "2023-08-01T14:33:25.557503Z"}]
    mean_response_time = calculate_mean_multiple_delta_datetime_formatted(started_claims, 'publish_date', 'start_date')

    started_claims = [{'publish_date': "2023-07-01T11:26:00.210087Z", "end_date": "2023-08-02T10:33:25.557503Z"}]
    mean_ending_time = calculate_mean_multiple_delta_datetime_formatted(started_claims, 'publish_date', 'end_date')

    claims = [{"category": 1}, {"category": 1}, {"category": 2}]
    categories = [{'name': 'Conflicts', 'id': 1}, {'name': 'Risques', 'id': 2}]
    most_opened_claim_category = find_most_occurred_claim_category(claims, categories)

    claims = [{"category": 2}, {"category": 2}, {"category": 2}]
    categories = [{'name': 'Conflicts', 'id': 1}, {'name': 'Risques', 'id': 2}]
    most_closed_claim_category = find_most_occurred_claim_category(claims, categories)

    # We don't need to use different values of date
    published_claims = [
        {'publish_date': '2023-08-01T14:33:25.557503Z'},
        {'publish_date': '2023-08-01T14:33:25.557503Z'},
        {'publish_date': '2023-08-01T14:33:25.557503Z', 'close_date': '2023-08-01T14:33:25.557503Z'},
        {'publish_date': '2023-08-01T14:33:25.557503Z', 'close_date': '2023-08-01T14:33:25.557503Z'}
    ]

    closed_claims = [
        {'publish_date': '2023-08-01T14:33:25.557503Z', 'close_date': '2023-08-01T14:33:25.557503Z'},
        {'publish_date': '2023-08-01T14:33:25.557503Z', 'close_date': '2023-08-01T14:33:25.557503Z'}
    ]

    performance = calculate_best_performances_by_hours(closed_claims, published_claims,
                                                       48)

    published_claims = [
        {'publish_date': '2023-01-01T14:33:25.557503Z'},
        {'publish_date': '2023-01-01T14:33:25.557503Z'},
        {'publish_date': '2023-02-01T14:33:25.557503Z', 'close_date': '2023-08-01T14:33:25.557503Z'},
        {'publish_date': '2023-01-01T14:33:25.557503Z', 'close_date': '2023-08-01T14:33:25.557503Z'},
        {'publish_date': '2023-03-01T14:33:25.557503Z', 'close_date': '2023-08-01T14:33:25.557503Z'},
        {'publish_date': '2023-05-01T14:33:25.557503Z', 'close_date': '2023-08-01T14:33:25.557503Z'}
    ]

    # Assuming the 'publish_date' attribute exists in each object
    gd = group_claims_by_publish_date(published_claims)
    bar_chart = {'data': list(gd.values()), 'labels': list(gd.keys())}
    gd = group_claims_by_publish_date_cumuli(published_claims)
    line_chart = {'data': list(gd.values()), 'labels': list(gd.keys())}

    last_5_unclosed_claims = [
        {'id': 1, 'message': 'message1', 'publish_date': '2023-01-01T14:33:25.557503Z', 'status': 'pending'},
        {'id': 45, 'message': 'message2', 'publish_date': '2023-02-01T14:33:25.557503Z',
         'start_date': '2023-02-01T14:34:25.557503Z', 'status': 'proceed'},
        {'id': 33, 'message': 'message3', 'publish_date': '2023-03-01T14:33:25.557503Z',
         'start_date': '2023-03-01T14:34:25.557503Z', 'end_date': '2023-03-01T14:35:25.557503Z', 'status': 'finish'},
        {'id': 66, 'message': 'message4', 'publish_date': '2023-04-01T14:33:25.557503Z',
         'start_date': '2023-04-01T14:34:25.557503Z', 'status': 'proceed'},
        {'id': 98, 'message': 'message5', 'publish_date': '2023-05-01T14:33:25.557503Z',
         'start_date': '2023-05-01T14:34:25.557503Z', 'end_date': '2023-05-01T14:35:25.557503Z', 'status': 'finish'}

    ]

    last_5_closed_claims = [

        {'id': 22, 'message': 'message2', 'publish_date': '2023-02-01T14:33:25.557503Z',
         'start_date': '2023-02-01T14:33:25.557503Z', 'end_date': '2023-02-01T14:55:25.557503Z', 'status': 'finish',
         'close': True},
        {'id': 45, 'message': 'message2', 'publish_date': '2023-02-01T14:33:25.557503Z',
         'start_date': '2023-02-01T14:34:25.557503Z', 'end_date': '2023-02-01T14:35:25.557503Z', 'status': 'finish',
         'close': True},
        {'id': 33, 'message': 'message3', 'publish_date': '2023-03-01T14:33:25.557503Z',
         'start_date': '2023-03-01T14:34:25.557503Z', 'end_date': '2023-03-01T14:35:25.557503Z', 'status': 'finish',
         'close': True},
        {'id': 66, 'message': 'message4', 'publish_date': '2023-04-01T14:33:25.557503Z',
         'start_date': '2023-04-01T14:34:25.557503Z', 'end_date': '2023-04-01T14:35:25.557503Z', 'status': 'finish',
         'close': True},
        {'id': 98, 'message': 'message5', 'publish_date': '2023-05-01T14:33:25.557503Z',
         'start_date': '2023-05-01T14:34:25.557503Z', 'end_date': '2023-05-01T14:35:25.557503Z', 'status': 'finish',
         'close': True}

    ]

    return {
        'activated_employees': 20,
        'activated_employees_percentage': "20%",
        'total_employees': 100,
        'activated_units': 15,
        'activated_units_percentage': "33.33%",
        'total_units': 45,
        'mean_response_time': mean_response_time,
        'mean_ending_time': mean_ending_time,
        'most_opened_claim_category': most_opened_claim_category['category']['name'],
        'most_opened_claim_category_times': most_opened_claim_category['times'],
        'last_five_unclosed_claims': last_5_unclosed_claims,
        'most_closed_claim_category': most_closed_claim_category['category']['name'],
        'most_closed_claim_category_times': most_closed_claim_category['times'],
        'last_five_closed_claims': last_5_closed_claims,
        'performance': performance,
        'bar_chart': bar_chart,
        'line_chart': line_chart
    }


def dashboard_data():
    """
    Fetch and process data to generate the dashboard statistics.

    Returns:
        dict: A dictionary containing various statistics for the dashboard.

    The function fetches data from external sources and processes it to generate various statistics for the dashboard.

    The generated statistics include:
    - Number and percentage of activated employees and units
    - Mean response time and mean ending time for claims
    - Most opened and most closed claim categories with their occurrence counts
    - Lists of last five unclosed and closed claims
    - Best performances based on closed and published claims within a specified hour range
    - Data for bar chart and line chart visualization

    The function returns a dictionary containing all the generated statistics.
    """
    # Fetch configuration data.
    config = repositories.get_configuration()

    # If configuration data is not available, return None.
    if not config:
        return None

    # Fetch data from the API.
    data = repositories.fetch_data_from_api()

    # Extract relevant data from the API response.
    claims = data[constants.CLAIMS]
    published_claims = list(filter(lambda el: el[constants.PUBLISH_DATE], claims))
    unclosed_claims = list(filter(lambda el: not el[constants.CLOSE], published_claims))
    closed_claims = list(filter(lambda el: el[constants.CLOSE], published_claims))
    ended_claims = list(filter(lambda el: el[constants.END_DATE], claims))
    started_claims = list(filter(lambda el: el[constants.START_DATE], claims))

    categories = data['categories']
    users = data['users']
    departments = data['departments']  # Assuming 'departments' is a list of departments obtained from somewhere

    # Generate data for the bar chart visualization.
    grouped_data = group_claims_by_publish_date(published_claims)
    bar_chart = {'data': list(grouped_data.values()), 'labels': list(grouped_data.keys())}

    # Generate data for the line chart visualization.
    grouped_data_cummul = group_claims_by_publish_date_cumuli(published_claims)
    line_chart = {'data': list(grouped_data_cummul.values()), 'labels': list(grouped_data_cummul.keys())}

    # Calculate and generate statistics for activated employees and units.
    activated_employees = count_activated_employees(published_claims, config.total_employees)
    activated_units = count_activated_units(users, len(departments))

    # Calculate mean response time and mean ending time for claims.
    mean_response_time = calculate_mean_multiple_delta_datetime_formatted(
        started_claims, constants.PUBLISH_DATE, constants.START_DATE)
    mean_ending_time = calculate_mean_multiple_delta_datetime_formatted(
        ended_claims, constants.PUBLISH_DATE, constants.END_DATE)

    # Find the most opened and most closed claim categories with their occurrence counts.
    most_opened_claim_category = find_most_occurred_claim_category(published_claims, categories)
    most_closed_claim_category = find_most_occurred_claim_category(closed_claims, categories)

    # Get the last five unclosed and closed claims sorted by some key (not specified in the code).
    last_five_unclosed_claims = sort_by_key(unclosed_claims)[0:5]
    last_five_closed_claims = sort_by_key(closed_claims)[0:5]

    # Calculate the best performances based on closed and published claims within a specified hour range.
    performance_by_hours = calculate_best_performances_by_hours(closed_claims, published_claims,
                                                                config.performance_hours_offset)

    # Construct and return the dashboard data as a dictionary.
    return {
        'activated_employees': activated_employees['number'],
        'activated_employees_percentage': activated_employees['percentage'],
        'total_employees': activated_employees['total'],
        'activated_units': activated_units['number'],
        'activated_units_percentage': activated_units['percentage'],
        'total_units': activated_units['total'],
        'mean_response_time': mean_response_time,
        'mean_ending_time': mean_ending_time,
        'most_opened_claim_category': most_opened_claim_category['category']['name'],
        'most_opened_claim_category_times': most_opened_claim_category['times'],
        'last_five_unclosed_claims': last_five_unclosed_claims,
        'most_closed_claim_category': most_closed_claim_category['category']['name'],
        'most_closed_claim_category_times': most_closed_claim_category['times'],
        'last_five_closed_claims': last_five_closed_claims,
        'performance': performance_by_hours,
        'bar_chart': bar_chart,
        'line_chart': line_chart
    }


def count_activated_employees(claims, total_employees):
    """
    Count the number of activated employees and calculate the percentage.

    Parameters:
        claims (list): A list of dictionaries containing claim data.
        total_employees (int): The total number of employees.

    Returns:
        dict: A dictionary containing the number of activated employees, percentage, and total employees.

    The function takes a list of dictionaries containing claim data and the total number of employees.
    It then counts the number of activated employees based on the 'employee' field in the claim data.
    The activated employees are calculated as the number of unique 'employee' values found in the 'claims' list.

    The function also calculates the percentage of activated employees out of the total employees and returns
    a dictionary containing the number of activated employees, percentage, and total employees.
    """
    # Initialize a list to store unique 'employee' values.
    employees_id = []

    # Iterate through each claim in the 'claims' list.
    for claim in claims:
        # Check if the 'employee' value of the claim is not already in the 'employees_id' list.
        if claim['employee'] not in employees_id:
            # Append the 'employee' value to the 'employees_id' list.
            employees_id.append(claim['employee'])

    # Calculate the number of activated employees (unique 'employee' values).
    activated_employees = len(employees_id)

    # Calculate the percentage of activated employees out of the total employees.
    activated_employees_percentage = (activated_employees / total_employees) * 100

    # Return the results as a dictionary.
    return {
        'number': activated_employees,
        'percentage': str(format_percentage(activated_employees_percentage)) + "%",
        'total': total_employees
    }


def count_activated_units(users, total_units):
    """
    Count the number of activated units and calculate the percentage.

    Parameters:
        users (list): A list of dictionaries containing user data.
        total_units (int): The total number of units.

    Returns:
        dict: A dictionary containing the number of activated units, percentage, and total units.

    The function takes a list of dictionaries containing user data and the total number of units.
    It then counts the number of activated units based on the 'department' field in the user data.
    The activated units are calculated as the number of unique 'department' values found in the 'users' list.

    The function also calculates the percentage of activated units out of the total units and returns
    a dictionary containing the number of activated units, percentage, and total units.

    If the total_units is greater than zero, it returns the results as calculated. If total_units is zero
    or less, it returns a default dictionary with the number of activated units set to the total_units,
    percentage as "{total_units}%", and the total units value itself.
    """
    if total_units > 0:
        # Initialize a list to store unique 'department' values.
        units_id = []

        # Iterate through each user in the 'users' list.
        for user in users:
            # Check if the 'department' value of the user is not already in the 'units_id' list.
            if user['department'] not in units_id:
                # Append the 'department' value to the 'units_id' list.
                units_id.append(user['department'])

        # Calculate the number of activated units (unique 'department' values).
        activated_units = len(units_id)

        # Calculate the percentage of activated units out of the total units.
        activated_units_percentage = (activated_units / total_units) * 100

        # Return the results as a dictionary.
        return {
            'number': activated_units,
            'percentage': str(format_percentage(activated_units_percentage)) + "%",
            'total': total_units
        }
    else:
        # Return a default dictionary when total_units is zero or less.
        return {
            'number': total_units,
            'percentage': f"{total_units}%",
            'total': total_units
        }


def find_most_occurred_claim_category(claims, categories):
    """
    Find the most occurred claim category from a list of claims and a list of categories.

    Parameters:
        claims (list): A list of dictionaries containing claim data.
        categories (list): A list of dictionaries representing claim categories.

    Returns:
        dict: A dictionary containing the most occurred claim category and its occurrence count.

    The function takes a list of dictionaries containing claim data and a list of dictionaries
    representing claim categories. It then finds the claim category that occurs the most among
    the claims and returns a dictionary containing the most occurred claim category and its
    occurrence count.

    If either the 'claims' or 'categories' list is empty or None, it returns a default dictionary
    with a "No Category Found" entry and a times count of -1.
    """
    if claims and categories:
        # Initialize variables to store the maximum occurrence count and the most occurred category.
        max_occurrence = 0
        most_occurred_category = {}

        # Iterate through each category in the 'categories' list.
        for cat in categories:
            # Count the number of occurrences of the current category in the 'claims' list.
            occurrences = sum(claim['category'] == cat['id'] for claim in claims)

            # Check if the current category has more occurrences than the previous maximum.
            if occurrences > max_occurrence:
                most_occurred_category = cat
                max_occurrence = occurrences

        # Return the dictionary containing the most occurred category and its occurrence count.
        return {'category': most_occurred_category, 'times': max_occurrence}
    else:
        # Return a default dictionary when either the 'claims' or 'categories' list is empty or None.
        return {'category': {'name': 'No Category Found'}, 'times': -1}


def calculate_best_performances_by_hours(closed_claims, published_claims, performance_hour_offset):
    """
    Calculate the best performances based on closed and published claims within a specified hour range.

    Parameters:
        closed_claims (list): A list of dictionaries containing closed claim data.
        published_claims (list): A list of dictionaries containing published claim data.
        performance_hour_offset (int): The offset in hours for performance calculations.

    Returns:
        dict: A dictionary containing the calculated best performances.

    The function calculates the best performances based on closed and published claims within
    a specified hour range. It takes the following steps:

    1. If there are closed claims, it calculates the number of closed claims and published claims
       that fall within the specified hour range, using the 'is_datetime_between' function.

    2. It calculates the percentage of closed claims out of published claims, rounded to two
       decimal places, and converts it to a percentage string.

    3. It returns a dictionary containing the counted closed claims, counted published claims,
       the calculated percentage, and the specified hours offset.

    If there are no closed claims, it returns a dictionary with zero counted closed claims, the
    total number of published claims, a percentage of "0%", and the specified hours offset.
    """
    if closed_claims:
        # Get the current datetime.
        current_datetime = datetime.now()

        # Calculate the new datetime with the specified performance_hour_offset.
        new_datetime = sub_hours_from_datetime(current_datetime, performance_hour_offset)

        # Initialize counters for closed claims and published claims within the hour range.
        count_closed_claims = 0
        count_published_claims = 0

        # Count the number of closed claims and published claims within the hour range.
        for claim in closed_claims:
            if is_datetime_between(datetime.fromisoformat(claim["close_date"][:-1]), new_datetime, current_datetime):
                count_closed_claims += 1

        for claim in published_claims:
            if is_datetime_between(datetime.fromisoformat(claim["publish_date"][:-1]), new_datetime, current_datetime):
                count_published_claims += 1

        # Calculate the percentage of closed claims out of published claims.
        count_closed_claims_per = (count_closed_claims / count_published_claims) * 100

        # Return the results in a dictionary.
        return {
            'counted_closed_claims': count_closed_claims,
            'counted_published_claims': count_published_claims,
            'percentage': str(format_percentage(count_closed_claims_per)) + "%",
            'hours': performance_hour_offset
        }
    else:
        # Return results when there are no closed claims.
        return {
            'counted_closed_claims': len(closed_claims),
            'counted_published_claims': len(published_claims),
            'percentage': "0%",
            'hours': performance_hour_offset
        }


def group_claims_by_publish_date(claims):
    """
    Group claims data by the publish date, and count occurrences for each month.

    Parameters:
        claims (list): A list of dictionaries containing claim data.

    Returns:
        dict: A dictionary containing the count of claims occurrences for each month.

    The function takes a list of dictionaries containing claim data and groups the data by
    the publish date. It then uses the 'group_data_by_month' function to count the occurrences
    for each month based on the 'publish_date' key in the dictionaries. The resulting dictionary
    contains the count of claim occurrences for each month.
    """
    # Use the 'group_data_by_month' function to group claims by the 'publish_date' key.
    return group_data_by_month(claims, constants.PUBLISH_DATE)


def group_claims_by_publish_date_cumuli(claims):
    """
    Group claims data by the publish date and calculate cumulative occurrences for each month.

    Parameters:
        claims (list): A list of dictionaries containing claim data.

    Returns:
        dict: A dictionary containing the cumulative count of claims occurrences for each month.

    The function takes a list of dictionaries containing claim data and first groups the data by
    the publish date using the 'group_claims_by_publish_date' function. It then calculates the
    cumulative occurrences for each month and returns a dictionary containing the cumulative count
    of claim occurrences for each month.
    """
    # Group claims by the publish date using the 'group_claims_by_publish_date' function.
    grouped_claims = group_claims_by_publish_date(claims)

    # Calculate cumulative occurrences for each month and store them in 'cumulated_claims' dictionary.
    cumulated_claims = {}
    for i in range(1, len(grouped_claims) + 1):
        counter = 0
        for j in range(1, i + 1):
            counter = counter + list(grouped_claims.values())[j - 1]
        cumulated_claims[list(grouped_claims.keys())[i - 1]] = counter

    # Return the dictionary containing cumulative claim occurrences for each month.
    return cumulated_claims


def init_configuration_form():
    """
    Initialize the configuration form with initial data from the database.

    Returns:
        ConfigForm: An instance of the ConfigForm initialized with existing configuration data,
                    if available; otherwise, a new ConfigForm instance.

    The function initializes the configuration form with initial data from the database.
    It first attempts to retrieve the existing configuration from the database using the
    get_configuration() function from the repositories module.

    If an existing configuration is found, the function returns a ConfigForm instance
    initialized with the existing configuration data. The form fields 'total_employees_number',
    'total_unities_number', and 'performance_hours_offset' are set with the corresponding values
    from the configuration.

    If no existing configuration is found, the function returns a new, empty ConfigForm instance.
    """
    # Try to retrieve the existing configuration (if any).
    config = get_configuration()

    if config:
        # If an existing configuration is found, create a ConfigForm instance with the existing data.
        return ConfigForm(
            initial={
                'total_employees_number': config.total_employees,
                'total_unities_number': config.total_units,
                'performance_hours_offset': config.performance_hours_offset
            }
        )
    else:
        # If no existing configuration is found, return a new, empty ConfigForm instance.
        return ConfigForm()


def save_or_update_configuration(request):
    """
    Save or update the configuration settings based on the submitted form data.

    Parameters:
        request (HttpRequest): The HTTP request object containing form data.

    The function takes an HTTP request object and saves or updates the configuration settings
    based on the submitted form data. It uses a custom ConfigForm to validate the form data.

    If the form is valid, the function retrieves the existing configuration (if any) using
    the get_configuration() function from the repositories' module. If there is no existing
    configuration, it creates a new configuration using the create_configuration() function.

    If there is an existing configuration, the function updates it with the new form data using
    the update_configuration() function from the repositories' module.
    """
    # Create a ConfigForm instance with the submitted form data.
    form = ConfigForm(request.POST)

    # Check if the form data is valid.
    if not form.is_valid():
        # If the form is not valid, raise an exception with the form errors.
        raise Exception("Form data is not valid: {}".format(form.errors))

    # If the form is valid, continue with processing.
    config = get_configuration()

    if not config:
        create_configuration(form)
    else:
        update_configuration(config.id, form)
