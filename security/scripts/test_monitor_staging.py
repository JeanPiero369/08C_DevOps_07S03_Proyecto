import unittest
from unittest.mock import patch
from monitor_staging import query

class MonitorUrlTest(unittest.TestCase):
    def test_non_http_urls_and_embedded_credentials_are_rejected(self):
        for url in ('file:///etc/passwd', 'ftp://localhost/data', 'http://user:pass@localhost:9090', 'http:///missing-host'):
            with self.subTest(url=url), patch('monitor_staging.http.client.HTTPConnection') as connect:
                with self.assertRaises(ValueError):
                    query(url, 'up')
                connect.assert_not_called()

if __name__ == '__main__': unittest.main()
