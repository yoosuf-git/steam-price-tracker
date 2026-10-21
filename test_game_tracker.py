import unittest
from unittest.mock import Mock, patch
from io import StringIO

import game_tracker


class GameTrackerTests(unittest.TestCase):
    @patch("game_tracker.requests.get")
    def test_get_game_price_uses_data_price_final(self, mock_get):
        mock_response = Mock()
        mock_response.text = """
        <html>
            <head><title>Test Game</title></head>
            <body>
                <div class="game_purchase_price price" data-price-final="4999">$49.99</div>
            </body>
        </html>
        """
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        app_id, name, price = game_tracker.get_game_price("https://store.steampowered.com/app/123456/Test")

        self.assertEqual(app_id, "123456")
        self.assertEqual(name, "Test Game")
        self.assertEqual(price, 4999)

    @patch("game_tracker.requests.get")
    def test_get_game_price_falls_back_to_meta_price(self, mock_get):
        mock_response = Mock()
        mock_response.text = """
        <html>
            <head>
                <title>Meta Priced Game</title>
                <meta itemprop="price" content="29.99">
            </head>
            <body></body>
        </html>
        """
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        app_id, name, price = game_tracker.get_game_price("https://store.steampowered.com/app/98765/Test")

        self.assertEqual(app_id, "98765")
        self.assertEqual(name, "Meta Priced Game")
        self.assertEqual(price, 2999)

    @patch("builtins.open")
    @patch("game_tracker.analyse_with_gemini")
    def test_check_price_drop_uses_app_id_history(self, mock_analyse, mock_open):
        csv_data = (
            "2026-10-01,111,Some Other Name,6999\n"
            "2026-10-02,222,Tracked Name,1499\n"
        )
        mock_open.return_value.__enter__.return_value = StringIO(csv_data)

        game_tracker.check_price_drop("111", "Tracked Name", 4999)

        mock_analyse.assert_called_once_with("Tracked Name", 4999, 6999)

    @patch.dict("os.environ", {}, clear=True)
    @patch("builtins.print")
    def test_analyse_with_gemini_skips_without_api_key(self, mock_print):
        game_tracker.analyse_with_gemini("Game", 1000, 2000)
        mock_print.assert_any_call("Skipping Gemini analysis: GEMINI_API_KEY not set")


if __name__ == "__main__":
    unittest.main()
