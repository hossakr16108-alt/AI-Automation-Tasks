import unittest

from website_scraper import scrape_website


class TestWebsiteScraper(unittest.TestCase):

    def test_valid_website(self):
        """
        Test that a valid website can be scraped.
        """

        result = scrape_website(
            "https://example.com"
        )

        self.assertIsInstance(
            result,
            dict
        )

        self.assertIn(
            "title",
            result
        )

        self.assertIn(
            "visible_text",
            result
        )

        self.assertIn(
            "links",
            result
        )

    def test_invalid_url(self):
        """
        Test that an invalid URL raises an error.
        """

        with self.assertRaises(Exception):

            scrape_website(
                "this-is-not-a-valid-url"
            )


if __name__ == "__main__":
    unittest.main()
    