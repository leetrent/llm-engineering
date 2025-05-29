import unittest
from unittest.mock import patch, Mock
from website_links import get_links_from_url

class TestWebsiteLinks(unittest.TestCase):
    @patch("website_links.requests.get")
    def test_get_links_from_url(self, mock_get):
        html = """
        <html>
            <body>
                <a href="https://example.com/page1">Page 1</a>
                <a href="/page2">Page 2</a>
                <a href="">Empty</a>
                <a>No href</a>
            </body>
        </html>
        """

        # Create a mock response object with our test HTML
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = html.encode("utf-8")
        mock_get.return_value = mock_response

        url = "https://example.com"
        expected_links = [
            "https://example.com/page1",
            "https://example.com/page2"
        ]

        actual_links = get_links_from_url(url)

        self.assertEqual(actual_links, expected_links)

if __name__ == "__main__":
    unittest.main()
