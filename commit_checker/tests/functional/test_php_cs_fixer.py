import os
import subprocess
import unittest

from commit_checker.lib import TmpDirectory
from commit_checker.tests.support import GitRepo


class FunctionalTestPhpCsFixer(unittest.TestCase):
    def setUp(self):
        self.__test_repo_dir = TmpDirectory.create_tmp_dir()
        self.__repo = GitRepo(self.__test_repo_dir)

    def test_rejected_push(self):
        command = 'git rev-parse HEAD'
        new_rev = subprocess.check_output(['bash', '-c', command], cwd=self.__test_repo_dir).split("\n")[0]
        command = 'git rev-parse HEAD~1'
        old_rev = subprocess.check_output(['bash', '-c', command], cwd=self.__test_repo_dir).split("\n")[0]

        script_path = os.path.abspath(os.path.dirname(__file__) + '/../../')
        command = 'echo %s %s %s | python %s' % (old_rev, new_rev, 'refs/heads/master', script_path)

        dev_null = open(os.devnull, 'w')
        exit_code = subprocess.call(['bash', '-c', command], cwd=self.__test_repo_dir, stdout=dev_null, stderr=dev_null)

        self.assertEqual(exit_code, 108)

    def test_pass_push(self):
        command = 'git rev-parse HEAD~1'
        new_rev = subprocess.check_output(['bash', '-c', command], cwd=self.__test_repo_dir).split("\n")[0]
        command = 'git rev-parse HEAD~2'
        old_rev = subprocess.check_output(['bash', '-c', command], cwd=self.__test_repo_dir).split("\n")[0]

        script_path = os.path.abspath(os.path.dirname(__file__) + '/../../')
        command = 'echo %s %s %s | python %s' % (old_rev, new_rev, 'refs/heads/master', script_path)

        dev_null = open(os.devnull, 'w')
        exit_code = subprocess.call(['bash', '-c', command], cwd=self.__test_repo_dir, stdout=dev_null, stderr=dev_null)

        self.assertEqual(exit_code, 0)
