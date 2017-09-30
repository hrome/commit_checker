from argparse import ArgumentParser


class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        self.parser = ArgumentParser()
        self.parser.add_argument('--php-cs-fixer',
                                 dest='php_cs_fixer_enabled',
                                 action='store_true',
                                 default=False,
                                 help='Enable php-cs-fixer')
        self.parser.add_argument('--php-cs-fixer-config-path',
                                 dest='php_cs_fixer_config_path',
                                 default='.php_cs',
                                 help='php-cs-fixer config file (Default: .php_cs)')

        self.parser.add_argument('--php-cs-fixer-executable',
                                 dest='php_cs_fixer_executable',
                                 default='/usr/local/bin/php-cs-fixer-v2',
                                 help='php-cs-fixer config file (Default: /usr/local/bin/php-cs-fixer-v2)')

    def parse(self, args):
        known, unknown = self.parser.parse_known_args(args)

        return known
