import unittest

from app_protocols.dto import AppStartingParams


class UtilsTesting(unittest.TestCase):
    def test_app_params(self):
        app_params = AppStartingParams(
            bind_host="127.0.0.1",
            bind_port=8000,
            config_file=None,
        )
        self.assertEqual(app_params.bind_host, "127.0.0.1")
        self.assertEqual(app_params.bind_port, 8000)
        self.assertEqual(app_params.config_file, None)


if __name__ == "__main__":
    unittest.main()
