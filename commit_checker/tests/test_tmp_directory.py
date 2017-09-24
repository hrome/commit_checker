import os
import unittest

from commit_checker.lib import TmpDirectory


class TestTmpDirectory(unittest.TestCase):
    def test_create_dir(self):
        tmp_dir_path = TmpDirectory.create_tmp_dir()
        self.assertTrue(os.path.isdir(tmp_dir_path))


if __name__ == '__main__':
    unittest.main()
