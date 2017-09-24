import subprocess
import unittest

from commit_checker.lib import TmpDirectory
from commit_checker.lib.git_repository import GitRepository


class TestGitRepository(unittest.TestCase):
    def setUp(self):
        self.repo_dir = TmpDirectory.create_tmp_dir()
        command = 'cd %s && git init && git commit --allow-empty -m "Initial commit"' % self.repo_dir
        print subprocess.check_call(['bash', '-c', command])

    def test_getting_default_branch_name(self):
        repo = GitRepository(self.repo_dir)
        default_branch_name = repo.get_default_branch_name()
        self.assertEqual(default_branch_name, 'master')
