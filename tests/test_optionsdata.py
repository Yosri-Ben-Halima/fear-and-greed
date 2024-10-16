import unittest
import os
import pickle
import pandas as pd
from src.marketdata import OptionsData


class TestOptionsData(unittest.TestCase):
    def setUp(self):
        self.test_currency = "BTC"
        self.test_start = "2023-01-01"
        self.test_end = "2023-12-31"

        self.options_data = OptionsData(
            currency=self.test_currency, start=self.test_start, end=self.test_end
        )

        self.file_name = "test_options_data.pkl"

    def test_initialization(self):
        """Test that the OptionsData initializes correctly."""
        self.assertEqual(self.options_data.currency, self.test_currency)
        self.assertEqual(self.options_data.start, self.test_start)
        self.assertEqual(self.options_data.end, self.test_end)
        self.assertIsInstance(self.options_data.historical_data, pd.DataFrame)

    def test_currency_property(self):
        """Test the currency property getter and setter."""
        old_currency_data = self.options_data.historical_data
        self.options_data.currency = "ETH"
        self.assertEqual(self.options_data.currency, "ETH")
        self.assertFalse(self.options_data.historical_data.equals(old_currency_data))

    def test_start_property(self):
        """Test the start date property getter and setter."""

        old_length = len(self.options_data.historical_data)

        # Test case for setting an later start date
        self.options_data.start = "2023-06-01"
        self.assertEqual(self.options_data.start, "2023-06-01")
        self.assertTrue((self.options_data.historical_data.index >= "2023-06-01").all())

        # Test case for setting an earlier start date
        self.options_data.start = "2022-12-31"
        self.assertEqual(self.options_data.start, "2022-12-31")
        self.assertGreater(len(self.options_data.historical_data), old_length)


    def test_end_property(self):
        """Test the end date property getter and setter."""
        old_length = len(self.options_data.historical_data)

        # Test case for setting an earlier start date
        self.options_data.end = "2023-11-30"
        self.assertEqual(self.options_data.end, "2023-11-30")
        self.assertTrue((self.options_data.historical_data.index <= "2023-11-30").all())

        # Test case for setting an earlier end date
        self.options_data.end = "2023-01-15"
        self.assertEqual(self.options_data.end, "2023-01-15")
        self.assertLess(len(self.options_data.historical_data), old_length)

    def test_historical_data(self):
        """Test that historical data contains the expected date range."""
        historical_data = self.options_data.historical_data
        self.assertTrue(historical_data.index.min() >= pd.to_datetime(self.test_start))
        self.assertTrue(historical_data.index.max() <= pd.to_datetime(self.test_end))

    def tearDown(self):
        """
        Clean up any generated files after each test case.
        """
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def test_save_method(self):
        """
        Test that the save method works correctly and adds .pkl if not present.
        """
        self.options_data.save(self.file_name[:-4])  # Test without .pkl extension
        self.assertTrue(os.path.exists(self.file_name))  # Check file exists
        with open(self.file_name, "rb") as f:
            loaded_data = pickle.load(f)
        self.assertEqual(
            loaded_data.currency, self.options_data.currency
        )  # Check that the data is saved correctly

    def test_load_method(self):
        """
        Test that the load method works correctly and loads the saved object.
        """
        self.options_data.save(self.file_name)
        loaded_options_data = OptionsData.load(self.file_name)

        self.assertEqual(loaded_options_data.currency, self.options_data.currency)
        self.assertEqual(loaded_options_data.start, self.options_data.start)
        self.assertEqual(loaded_options_data.end, self.options_data.end)

    def test_save_load_without_extension(self):
        """
        Test save and load methods when file_name does not have .pkl extension.
        """
        file_name_no_extension = "test_options_data"
        self.options_data.save(file_name_no_extension)
        self.assertTrue(os.path.exists(file_name_no_extension + ".pkl"))

        loaded_options_data = OptionsData.load(file_name_no_extension)
        self.assertEqual(loaded_options_data.currency, self.options_data.currency)


if __name__ == "__main__":
    unittest.main()
