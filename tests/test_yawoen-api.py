from unittest import TestCase, mock
from unittest.mock import patch, mock_open
from yawoen_api import _load_csv, _load_website_data

class TestInfluxBackend(TestCase):
    """Test methods in Influx Backend."""

    @patch("builtins.open", mock_open(read_data='AbcD,123456'))
    def test_load_csv_success(self):
        """Unit test sucess of method '_load_csv'."""
        file_path = 'yawoen_api/q1_catalog.csv'
        result = _load_csv(file_path)

        self.assertEqual(result, 'Data loaded from CSV file.')


    @patch("os.path.exists", side_effect=[False])
    def test_load_csv_fail(self, mock_exists):
        """Unit test fail case of '_load_csv' with invalid input file."""
        file_path = 'yawoen_api/q3_catalog.csv'
        result = _load_csv(file_path)

        expected_result = (f"Error loading data from file '{file_path}'.\n"
                           "The file does not exist!")

        self.assertEqual(result, expected_result)


    @patch("builtins.open", mock_open(read_data='ABCD,123456,www.abcd.com'))
    def test_load_website_data_success(self):
        """Unit test sucess of method '_load_website_data'."""
        file_path = 'yawoen_api/q2_clientData.csv'
        result = _load_website_data(file_path)

        self.assertEqual(result, 'Website data loaded!')


    @patch("os.path.exists", side_effect=[False])
    def test_load_data_website_fail(self, mock_exists):
        """Unit test fail case of '_load_website_data' with invalid input file."""
        file_path = 'yawoen_api/q4_clientData.csv'
        result = _load_website_data(file_path)

        expected_result = (f"Error loading the website data from file '{file_path}'.\n"
                "The file does not exist!")

        self.assertEqual(result, expected_result)
