import tempfile
import unittest
from pathlib import Path

import app as website


class StartupSmokeTest(unittest.TestCase):
    def test_public_routes_start_with_fresh_database(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            website.app.config['DATABASE'] = str(Path(tmpdir) / 'fresh.db')
            website.app.config['TESTING'] = True

            client = website.app.test_client()
            for route in ['/', '/about', '/ai_projects', '/academic_research/', '/investment_research/', '/contact', '/admin/login']:
                with self.subTest(route=route):
                    self.assertEqual(client.get(route).status_code, 200)

            for route in ['/academic_research/1', '/academic_research/7', '/investment_research/1', '/ai_projects/investment-research-hub']:
                with self.subTest(route=route):
                    self.assertEqual(client.get(route).status_code, 200)

            self.assertEqual(client.get('/trading').status_code, 404)
            self.assertEqual(client.get('/ai_projects/not-real').status_code, 404)


if __name__ == '__main__':
    unittest.main()
