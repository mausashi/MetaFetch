import unittest
from unittest.mock import patch, Mock
from fetchSave import fetch_url, collect_metadata, sanitize_filename, download_assets
import requests

class TestFetchSave(unittest.TestCase):

    # Tests for fetch_url
    @patch('fetchSave.requests.get')
    def test_fetch_url_success(self, mock_get):
        # Mock response object
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response

        html_content, filename, domain = fetch_url('https://example.com')

        self.assertEqual(filename, 'example.com.html')
        self.assertEqual(domain, 'example.com')
        self.assertEqual(html_content, "<html></html>")

    @patch('fetchSave.requests.get')
    def test_fetch_url_failure(self, mock_get):
        # Simulate a request failure
        mock_get.side_effect = requests.RequestException("Request failed")

        html_content, filename, domain = fetch_url('https://example.com')

        self.assertIsNone(html_content)
        self.assertIsNone(filename)
        self.assertIsNone(domain)

    # Tests for collect_metadata
    def test_collect_metadata(self):
        html_content = '''
        <html>
            <body>
                <a href="#">Link 1</a>
                <a href="#">Link 2</a>
                <img src="image.jpg" />
            </body>
        </html>
        '''
        num_links, num_images, last_fetch = collect_metadata(html_content)

        self.assertEqual(num_links, 2)
        self.assertEqual(num_images, 1)
        self.assertTrue("UTC" in last_fetch)

    # Tests for sanitize_filename
    def test_sanitize_filename(self):
        self.assertEqual(sanitize_filename('invalid<>filename'), 'invalid__filename')
        self.assertEqual(sanitize_filename('test|file?name*'), 'test_file_name_')
        self.assertEqual(sanitize_filename(''), '')

    # Optional: Tests for download_assets (can be a bit more complex and usually requires more mocking)

if __name__ == '__main__':
    unittest.main()
