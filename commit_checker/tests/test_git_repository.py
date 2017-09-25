import os
import subprocess
import unittest

from commit_checker.lib import TmpDirectory
from commit_checker.lib.git_repository import GitRepository


class TestGitRepository(unittest.TestCase):
    def setUp(self):
        self.__repo_dir = TmpDirectory.create_tmp_dir()
        command_list = [
            'git init',
            'git commit --allow-empty -m "Initial commit"',
            'echo 123 > 123',
            'echo test > test',
            'git add 123 test',
            'git commit -m "123 and test"',
            'echo test >> test',
            'git add test',
            'git commit -m "only test"',
        ]

        dev_null = open(os.devnull, 'w')
        for command in command_list:
            subprocess.check_call(['bash', '-c', command], cwd=self.__repo_dir, stdout=dev_null,
                                  stderr=subprocess.STDOUT)

    def test_getting_default_branch_name(self):
        repo = GitRepository(self.__repo_dir)
        default_branch_name = repo.get_default_branch_name()
        self.assertEqual(default_branch_name, 'master')

    def test_getting_changed_file_names(self):
        repo = GitRepository(self.__repo_dir)
        command = 'git rev-parse HEAD'
        new_rev = subprocess.check_output(['bash', '-c', command], cwd=self.__repo_dir).split("\n")[0]
        command = 'git rev-parse HEAD~2'
        old_rev = subprocess.check_output(['bash', '-c', command], cwd=self.__repo_dir).split("\n")[0]
        changed_files = repo.get_changed_file_names(old_rev, new_rev)
        self.assertItemsEqual(changed_files, ['123', 'test'])
