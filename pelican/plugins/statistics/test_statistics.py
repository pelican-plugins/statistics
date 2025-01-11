import unittest

from pelican.contents import Article, Page

from . import statistics


class TestStatistics(unittest.TestCase):
    """Test the Statistics plugin."""

    def setUp(self):
        """Set up the test."""
        super().setUp()

    def test_article_calculate_stats(self):
        """Test the calculate_stats function with an Article."""
        args = {
            "content": "This is a test article.",
            "metadata": {
                "summary": "detailed summary",
            },
        }
        article = Article(**args)
        statistics.calculate_stats(article)
        self.assertEqual(article.statistics["wc"], 5)
        self.assertEqual(article.stats["wc"], 5)

    def test_page_calculate_stats(self):
        """Test the calculate_stats function with a Page."""
        args = {
            "content": "This is a test page.",
            "metadata": {
                "summary": "detailed summary",
            },
        }
        page = Page(**args)
        page._content = "This is a test page."
        statistics.calculate_stats(page)
        self.assertEqual(page.statistics["wc"], 5)
        self.assertEqual(page.stats["wc"], 5)


if __name__ == "__main__":
    unittest.main()
