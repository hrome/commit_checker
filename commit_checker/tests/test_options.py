import unittest

from commit_checker.lib import Options


class TestCommandLineParameters(unittest.TestCase):
    def setUp(self):
        self.options = Options()

    def test_defaults_options_are_set(self):
        config = self.options.parse([])
        self.assertEqual(config.binary_check_enabled, False)
        self.assertEqual(config.php_cs_fixer_enabled, False)
        self.assertEqual(config.php_cs_fixer_config_path, '.php_cs')
        self.assertEqual(config.php_cs_fixer_executable, '/usr/local/bin/php-cs-fixer-v2')

    def test_set_options(self):
        config = self.options.parse([
            '--binary-check',
            '--php-cs-fixer',
            '--php-cs-fixer-config-path', 'test',
            '--php-cs-fixer-executable', 'php-cs-fixer'
        ]
        )

        self.assertEqual(config.binary_check_enabled, True)
        self.assertEqual(config.php_cs_fixer_enabled, True)
        self.assertEqual(config.php_cs_fixer_config_path, 'test')
        self.assertEqual(config.php_cs_fixer_executable, 'php-cs-fixer')


if __name__ == '__main__':
    unittest.main()
