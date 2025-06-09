import unittest
from unittest.mock import patch
from datetime import datetime
import pandas as pd
from scripts.play_store_scraper import fetch_reviews


class TestFetchReviews(unittest.TestCase):

    @patch('scripts.scraper.reviews')
    def test_fetch_reviews_success(self, mock_reviews):
        mock_reviews.return_value = (
            [{'content': 'Good app', 'score': 5,
                'at': datetime(2024, 1, 1)}], None
        )

        df = fetch_reviews('com.example.app', 'Bank X')

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 1)
        self.assertEqual(df.iloc[0]['review'], 'Good app')
        self.assertEqual(df.iloc[0]['rating'], 5)
        self.assertEqual(df.iloc[0]['bank'], 'Bank X')
        self.assertEqual(df.iloc[0]['source'], 'Google Play')

    @patch('scripts.scraper.reviews', side_effect=Exception("API failed"))
    def test_fetch_reviews_failure(self, mock_reviews):
        df = fetch_reviews('com.fake.app', 'Fake Bank')
        self.assertTrue(df.empty)
