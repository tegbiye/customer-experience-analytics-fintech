import unittest
import pandas as pd
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime
from scripts.preprocess import (
    load_csv, clean_data,
    balance_review, combine_dataframes, save_cleand_data
)


class TestDataProcessing(unittest.TestCase):

    @patch('pandas.read_csv')
    def test_load_csv_success(self, mock_read_csv):
        mock_df = pd.DataFrame({'col': [1, 2]})
        mock_read_csv.return_value = mock_df
        df = load_csv('fake_path.csv')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)

    @patch('pandas.read_csv', side_effect=Exception("File not found"))
    def test_load_csv_failure(self, mock_read_csv):
        result = load_csv('bad_path.csv')
        self.assertEqual(result, [])

    def test_clean_data(self):
        raw_data = {
            'review_text': [' Great app ', None, 'Great app'],
            'bank_name': [' Bank A ', 'Bank A', 'Bank A'],
            'date': ['2024-01-01', 'invalid', '2024-01-01'],
            'source': [' Google Play ', 'Google Play', 'Google Play']
        }
        df = pd.DataFrame(raw_data)
        cleaned_df = clean_data(df)
        self.assertEqual(len(cleaned_df), 1)
        self.assertTrue(all(cleaned_df.columns == [
                        'review_text', 'bank_name', 'date', 'source']))

    def test_balance_review(self):
        df = pd.DataFrame({
            'review_text': ['review'] * 5,
            'bank_name': ['Bank A'] * 5,
            'date': [datetime.today()] * 5,
            'source': ['Google Play'] * 5
        })
        balanced_df = balance_review(df, count=10)
        self.assertEqual(balanced_df.shape[0], 10)
        self.assertEqual(balanced_df['bank_name'].unique()[0], 'Bank A')

    def test_combine_dataframes(self):
        df1 = pd.DataFrame({'col': [1, 2]})
        df2 = pd.DataFrame({'col': [3, 4]})
        combined = combine_dataframes([df1, df2])
        self.assertEqual(combined.shape[0], 4)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_cleand_data_success(self, mock_file):
        df = pd.DataFrame({'col': [1, 2]})
        with patch.object(pd.DataFrame, 'to_csv', return_value=None) as mock_to_csv:
            save_cleand_data(df, 'output.csv')
            mock_to_csv.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    def test_save_cleand_data_failure(self, mock_file):
        df = pd.DataFrame({'col': [1, 2]})
        with patch.object(pd.DataFrame, 'to_csv', side_effect=Exception("Write error")):
            save_cleand_data(df, 'output.csv')  # Should not raise
