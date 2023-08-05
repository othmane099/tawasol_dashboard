import requests

from App.models import Configuration
from tawasol_dashboard.settings import env


def fetch_data_from_api():
    """
    Fetch data from an API using a GET request with authorization headers.

    Returns:
        dict: A dictionary containing the JSON response from the API.

    The method sends a GET request to the API endpoint specified in the 'BASE_URL' environment variable.
    It includes an authorization token in the request headers, retrieved from the 'AUTHORIZATION_TOKEN'
    environment variable.

    The response is expected to be in JSON format. The method sets the response encoding to 'utf-8' and
    returns the JSON data as a Python dictionary.
    """
    # Send a GET request to the API with the authorization token in the headers.
    response = requests.get(env('BASE_URL'), headers={'Authorization': f"Token {env('AUTHORIZATION_TOKEN')}"})

    # Set the response encoding to 'utf-8'.
    response.encoding = "utf-8"

    # Parse the JSON data and return it as a Python dictionary.
    return response.json()


def get_configuration():
    """
    Retrieve the configuration data from the database.

    Returns:
        Configuration or None: The Configuration object if found, otherwise returns None.

    This function queries the database for the Configuration object using the 'objects' manager of the
    Configuration model. It retrieves the first configuration object found in the database and returns it.
    If no configuration object is found, it returns None.
    """
    try:
        configuration = Configuration.objects.first()  # Retrieve the first Configuration object from the database
    except Configuration.DoesNotExist:
        configuration = None  # If no Configuration object is found, set 'configuration' to None

    return configuration


def create_configuration(form):
    """
    Create and save a new Configuration object based on the form data.

    Args:
        form (ConfigForm): The form containing cleaned data for creating the Configuration object.

    This function takes a ConfigForm instance as input, which contains cleaned data for creating a new
    Configuration object. It creates a new Configuration model instance with the provided data and saves it
    to the database.
    """
    # Extract the cleaned data from the form.
    total_employees = form.cleaned_data['total_employees_number']
    total_units = form.cleaned_data['total_unities_number']
    performance_hours_offset = form.cleaned_data['performance_hours_offset']

    # Create a new Configuration model instance with the extracted data.
    config = Configuration(
        total_employees=total_employees,
        total_units=total_units,
        performance_hours_offset=performance_hours_offset
    )

    # Save the new Configuration object to the database.
    config.save()


def update_configuration(config_id, form):
    """
    Update the Configuration object with the provided ID using the form data.

    Args:
        config_id (int): The ID of the Configuration object to update.
        form (ConfigForm): The form containing cleaned data for updating the Configuration object.

    Raises:
        Configuration.DoesNotExist: If the specified Configuration object does not exist.

    This function takes the ID of the Configuration object to update and a ConfigForm instance with cleaned data
    for the update. It retrieves the existing Configuration object from the database based on the provided ID,
    updates its fields with the new data from the form, and saves the updated Configuration object to the database.
    If the specified Configuration object does not exist, it raises a Configuration.DoesNotExist exception.
    """
    try:
        # Retrieve the existing Configuration object based on the provided ID.
        config = Configuration.objects.get(id=config_id)

        # Update the fields of the existing Configuration object with the cleaned data from the form.
        config.total_employees = form.cleaned_data['total_employees_number']
        config.total_units = form.cleaned_data['total_unities_number']
        config.performance_hours_offset = form.cleaned_data['performance_hours_offset']

        # Save the updated Configuration object to the database.
        config.save()
    except Configuration.DoesNotExist:
        # If the specified Configuration object does not exist, raise a Configuration.DoesNotExist exception.
        raise Configuration.DoesNotExist("Configuration with the specified ID does not exist.")