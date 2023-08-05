from datetime import datetime, timedelta
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from App import helpers
from App import services
from App.forms import ConfigForm
from App.models import Configuration


# Create your tests here.

class ServicesTest(TestCase):
    def test_count_activated_employees(self):
        claims = [{'employee': 1}, {'employee': 2}, {'employee': 1}]
        total_employees = 5
        result = services.count_activated_employees(claims, total_employees)
        self.assertEqual(result['number'], 2)
        self.assertEqual(result['total'], 5)
        self.assertEqual(result['percentage'], f'{40}%')

    def test_count_activated_employees_with_empty_claims(self):
        empty_claims = []
        total_employees = 1  # must be bigger than 0, initialized in config page
        result = services.count_activated_employees(empty_claims, total_employees)
        self.assertEqual(result['number'], 0)
        self.assertEqual(result['total'], 1)
        self.assertEqual(result['percentage'], f'{0}%')

    def test_count_activated_units(self):
        users = [{'department': 1}, {'department': 2}, {'department': 1}]
        departments = [{"id": 1, "name": "department1"}, {"id": 2, "name": "department2"}]
        result = services.count_activated_units(users, len(departments))
        self.assertEqual(result['number'], 2)
        self.assertEqual(result['total'], 2)
        self.assertEqual(result['percentage'], f'{100}%')

        empty_users = []
        result = services.count_activated_units(empty_users, len(departments))
        self.assertEqual(result['number'], 0)
        self.assertEqual(result['total'], 2)
        self.assertEqual(result['percentage'], f'{0}%')

        # empty categories means empty users, to create new user must be assigned to specific category
        empty_categories = []
        result = services.count_activated_units(empty_users, len(empty_categories))
        self.assertEqual(result['number'], 0)
        self.assertEqual(result['total'], 0)
        self.assertEqual(result['percentage'], f'{0}%')

    def test_find_most_occurred_claim_category(self):
        NO_CATEGORY_FOUND = 'No Category Found'
        empty_claims = []
        empty_categories = []
        category = services.find_most_occurred_claim_category(empty_claims, empty_categories)
        self.assertEqual(NO_CATEGORY_FOUND, category['category']['name'])
        self.assertEqual(-1, category['times'])

        categories = [{'name': 'category one', 'id': 1}, {'name': 'category two', 'id': 2}]
        category = services.find_most_occurred_claim_category(empty_claims, categories)
        self.assertEqual(NO_CATEGORY_FOUND, category['category']['name'])
        self.assertEqual(-1, category['times'])

        claims = [{"category": 1}, {"category": 1}, {"category": 2}]
        categories = [{'name': 'category one', 'id': 1}, {'name': 'category two', 'id': 2}]
        category = services.find_most_occurred_claim_category(claims, categories)
        self.assertEqual('category one', category['category']['name'])
        self.assertEqual(2, category['times'])

    def test_calculate_best_performances_by_hours(self):
        empty_closed_claims = []
        empty_published_claims = []
        performance_hour_offset = 48  # it is constant must be initialized from the beginning in config page
        performance = services.calculate_best_performances_by_hours(empty_closed_claims, empty_published_claims,
                                                                    performance_hour_offset)
        self.assertEqual(0, performance['counted_closed_claims'])
        self.assertEqual(0, performance['counted_published_claims'])
        self.assertEqual("0%", performance['percentage'])
        self.assertEqual(performance_hour_offset, performance['hours'])

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

        performance = services.calculate_best_performances_by_hours(closed_claims, published_claims,
                                                                    performance_hour_offset)

        self.assertEqual(2, performance['counted_closed_claims'])
        self.assertEqual(4, performance['counted_published_claims'])
        self.assertEqual("50%", performance['percentage'])
        self.assertEqual(performance_hour_offset, performance['hours'])

    def test_group_claims_by_publish_date_cumuli(self):
        empty_published_claims = []

        data = services.group_claims_by_publish_date_cumuli(empty_published_claims)
        self.assertEqual('Jan', list(data.keys())[0])
        self.assertEqual(0, data['Jan'])

        # claim's date should be this year, otherwise it will not be counted
        published_claims = [
            {'publish_date': '2023-01-01T14:33:25.557503Z'},
            {'publish_date': '2023-01-01T14:33:25.557503Z'},
            {'publish_date': '2023-02-01T14:33:25.557503Z', 'close_date': '2023-08-01T14:33:25.557503Z'},
            {'publish_date': '2023-01-01T14:33:25.557503Z', 'close_date': '2023-08-01T14:33:25.557503Z'},
            {'publish_date': '2023-03-01T14:33:25.557503Z', 'close_date': '2023-08-01T14:33:25.557503Z'},
            {'publish_date': '2023-05-01T14:33:25.557503Z', 'close_date': '2023-08-01T14:33:25.557503Z'}
        ]

        # Assuming the 'publish_date' attribute exists in each object
        data = services.group_claims_by_publish_date_cumuli(published_claims)
        self.assertEqual('Jan', list(data.keys())[0])
        self.assertEqual(6, data['Aug'])

    @patch('App.services.get_configuration')
    def test_existing_configuration(self, mock_get_configuration):
        """
        Test if the form is initialized with existing configuration data.
        """
        # Create a mock configuration object with sample data
        mock_config = Configuration(total_employees=10, total_units=5, performance_hours_offset=3)

        # Set the return value of the mocked get_configuration function
        mock_get_configuration.return_value = mock_config

        # Check if the form is initialized with the existing configuration data
        form = services.init_configuration_form()

        self.assertIsInstance(form, ConfigForm)
        self.assertDictEqual(
            form.initial,
            {
                'total_employees_number': 10,
                'total_unities_number': 5,
                'performance_hours_offset': 3
            }
        )

    @patch('App.services.get_configuration')
    def test_no_existing_configuration(self, mock_get_configuration):
        """
        Test if the form is initialized with empty data when no existing configuration is found.
        """
        # Set the return value of the mocked get_configuration function to None (no existing config)
        mock_get_configuration.return_value = None

        # Check if the form is initialized with empty data
        form = services.init_configuration_form()
        self.assertIsInstance(form, ConfigForm)
        self.assertDictEqual(form.initial, {})


    @patch('App.services.get_configuration')
    @patch('App.services.create_configuration')
    @patch('App.services.update_configuration')
    def test_save_new_configuration(self, mock_update_config, mock_create_config, mock_get_config):
        """
        Test saving a new configuration.
        """
        mock_get_config.return_value = None  # Simulate no existing configuration
        form_data = {
            'total_employees_number': 10,
            'total_unities_number': 5,
            'performance_hours_offset': 3
        }
        response = self.client.post(reverse('config_form'), data=form_data)


        self.assertEqual(response.status_code, 302)
        self.assertTrue(mock_create_config.called)
        self.assertFalse(mock_update_config.called)

    @patch('App.services.get_configuration')
    @patch('App.services.create_configuration')
    @patch('App.services.update_configuration')
    def test_update_existing_configuration(self, mock_update_config, mock_create_config, mock_get_config):
        """
        Test updating an existing configuration.
        """
        existing_config = Configuration.objects.create(total_employees=5, total_units=3, performance_hours_offset=2)
        mock_get_config.return_value = existing_config
        form_data = {
            'total_employees_number': 10,
            'total_unities_number': 5,
            'performance_hours_offset': 3
        }
        response = self.client.post(reverse('config_form'), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(mock_create_config.called)
        self.assertTrue(mock_update_config.called)

    def test_invalid_form_data(self):
        """
        Test posting invalid form data.
        """
        form_data = {}  # Invalid form data

        with self.assertRaises(Exception):
            self.client.post(reverse('config_form'), data=form_data)


class HelpersTest(TestCase):
    def test_format_percentage(self):
        self.assertEqual('33.33', helpers.format_percentage(33.33))
        self.assertEqual('33', helpers.format_percentage(33.0))
        self.assertEqual('33.3', helpers.format_percentage(33.3))
        self.assertEqual('33.01', helpers.format_percentage(33.01))
        self.assertEqual('33.1', helpers.format_percentage(33.10))
        self.assertEqual('33', helpers.format_percentage(33.00))
        self.assertEqual('33', helpers.format_percentage(33.00000))
        self.assertEqual('33', helpers.format_percentage(33.001))
        self.assertEqual('57.69', helpers.format_percentage(57.692307692307686))

    """
        Test case for the 'calculate_mean_multiple_delta_datetime' function.
    """

    def test_calculate_mean_multiple_delta_datetime_formatted(self):
        empty_started_claims = []
        td = helpers.calculate_mean_multiple_delta_datetime_formatted(empty_started_claims, 'publish_date',
                                                                      'start_date')
        self.assertEqual(0, td['days'], 'days value with empty started claims list')
        self.assertEqual(0, td['hours'], 'hours value with empty started claims list')
        self.assertEqual(0, td['minutes'], 'minutes value with empty started claims list')

        # must started_claims have publish_date and start_date values
        started_claims = [{'publish_date': "2023-08-01T14:26:00.210087Z", "start_date": "2023-08-01T14:33:25.557503Z"}]
        td = helpers.calculate_mean_multiple_delta_datetime_formatted(started_claims, 'publish_date', 'start_date')
        self.assertEqual(0, td['days'], 'days value with started claims list')
        self.assertEqual(0, td['hours'], 'hours value with started claims list')
        self.assertEqual(7, td['minutes'], 'minutes value with started claims list')

    def test_calculate_mean_multiple_delta_datetime(self):
        # Test data: a list of dictionaries, each containing start and end date information.
        obj_list = [
            {'start_date': '2023-08-03T10:00:00Z', 'end_date': '2023-08-03T11:30:00Z'},
            {'start_date': '2023-08-03T12:00:00Z', 'end_date': '2023-08-03T13:30:00Z'},
            {'start_date': '2023-08-03T15:00:00Z', 'end_date': '2023-08-03T16:30:00Z'},
        ]
        start_date_key = 'start_date'
        end_date_key = 'end_date'

        # Call the 'calculate_mean_multiple_delta_datetime' function with the test data.
        mean_delta_time = helpers.calculate_mean_multiple_delta_datetime(obj_list, start_date_key, end_date_key)

        # Calculate the expected result manually based on the test data.
        expected_mean_delta_time = timedelta(hours=1, minutes=30)

        # Check if the result returned by the function matches the expected result.
        self.assertEqual(mean_delta_time, expected_mean_delta_time)

    def test_group_data_by_month(self):
        empty_published_claims = []

        data = helpers.group_data_by_month(empty_published_claims, 'date')
        self.assertEqual('Jan', list(data.keys())[0])
        self.assertEqual(0, data['Jan'])

        # claim's date should be this year, otherwise it will not be counted
        published_claims = [
            {'publish_date': '2023-01-01T14:33:25.557503Z'},
            {'publish_date': '2023-01-01T14:33:25.557503Z'},
            {'publish_date': '2023-02-01T14:33:25.557503Z', 'close_date': '2023-08-01T14:33:25.557503Z'},
            {'publish_date': '2023-01-01T14:33:25.557503Z', 'close_date': '2023-08-01T14:33:25.557503Z'},
            {'publish_date': '2023-03-01T14:33:25.557503Z', 'close_date': '2023-08-01T14:33:25.557503Z'},
            {'publish_date': '2023-05-01T14:33:25.557503Z', 'close_date': '2023-08-01T14:33:25.557503Z'}
        ]

        # Assuming the 'publish_date' attribute exists in each object
        data = helpers.group_data_by_month(published_claims, 'publish_date')
        self.assertEqual('Jan', list(data.keys())[0])
        self.assertEqual(3, data['Jan'])

    """
       Test case for the 'sub_hours_from_datetime' function.
       """

    def test_sub_hours_from_datetime(self):
        # Test data: a datetime object and the number of hours to subtract.
        original_datetime = datetime(2023, 8, 3, 12, 0, 0)
        hours_to_subtract = 30

        # Call the 'sub_hours_from_datetime' function with the test data.
        new_datetime = helpers.sub_hours_from_datetime(original_datetime, hours_to_subtract)

        # Calculate the expected result by manually subtracting the hours from the original datetime.
        expected_datetime = datetime(2023, 8, 2, 6, 0, 0)

        # Check if the result returned by the function matches the expected result.
        self.assertEqual(new_datetime, expected_datetime)

    """
        Test case for the 'is_datetime_between' function.
        """

    def test_is_datetime_between_within_range(self):
        # Test data: a datetime object, start_datetime, and end_datetime within the range.
        datetime_to_check = datetime(2023, 8, 3, 12, 0, 0)
        start_datetime = datetime(2023, 8, 3, 10, 0, 0)
        end_datetime = datetime(2023, 8, 3, 14, 0, 0)

        # Call the 'is_datetime_between' function with the test data.
        result = helpers.is_datetime_between(datetime_to_check, start_datetime, end_datetime)

        # Check if the result returned by the function is True, as the datetime is within the range.
        self.assertTrue(result)

    def test_is_datetime_between_outside_range(self):
        # Test data: a datetime object, start_datetime, and end_datetime outside the range.
        datetime_to_check = datetime(2023, 8, 3, 18, 30, 0)
        start_datetime = datetime(2023, 8, 3, 10, 0, 0)
        end_datetime = datetime(2023, 8, 3, 14, 0, 0)

        # Call the 'is_datetime_between' function with the test data.
        result = helpers.is_datetime_between(datetime_to_check, start_datetime, end_datetime)

        # Check if the result returned by the function is False, as the datetime is outside the range.
        self.assertFalse(result)

    """
    Test case for the 'parse_string_datetime' function.
    """

    def test_parse_string_datetime_valid_format_1(self):
        # Test data: a valid datetime string in format '%Y-%m-%dT%H:%M:%SZ'.
        date_str = '2023-08-03T12:34:56Z'

        # Call the 'parse_string_datetime' function with the test data.
        date_obj = helpers.parse_string_datetime(date_str)

        # Calculate the expected result manually based on the test data.
        expected_date_obj = datetime(2023, 8, 3, 12, 34, 56)

        # Check if the result returned by the function matches the expected result.
        self.assertEqual(date_obj, expected_date_obj)

    def test_parse_string_datetime_valid_format_2(self):
        # Test data: a valid datetime string in format '%Y-%m-%dT%H:%M:%S.%fZ'.
        date_str = '2023-08-03T12:34:56.789Z'

        # Call the 'parse_string_datetime' function with the test data.
        date_obj = helpers.parse_string_datetime(date_str)

        # Calculate the expected result manually based on the test data.
        expected_date_obj = datetime(2023, 8, 3, 12, 34, 56, 789000)

        # Check if the result returned by the function matches the expected result.
        self.assertEqual(date_obj, expected_date_obj)

    def test_parse_string_datetime_invalid_format(self):
        # Test data: an invalid datetime string that does not match any of the formats.
        date_str = '2023-08-03 12:34:56'

        # Call the 'parse_string_datetime' function with the test data and expect a ValueError.
        with self.assertRaises(ValueError):
            helpers.parse_string_datetime(date_str)
