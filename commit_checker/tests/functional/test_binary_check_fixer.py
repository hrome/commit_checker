import os
import unittest
from subprocess import Popen, PIPE

from commit_checker.lib import TmpDirectory
from commit_checker.tests.support import GitRepo


class FunctionalTestBinaryCheckFixer(unittest.TestCase):
    def setUp(self):
        self.__test_repo_dir = TmpDirectory.create_tmp_dir()
        self.__repo = GitRepo(self.__test_repo_dir)
        self.__script_path = os.path.abspath(os.path.dirname(__file__) + '/../../')

    def test_rejected_push(self):
        new_rev = self.__repo.parse_rev('HEAD')
        old_rev = self.__repo.parse_rev('HEAD~3')

        command = 'python %s --binary-check' % self.__script_path

        p = Popen(['bash', '-c', command], cwd=self.__test_repo_dir, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate("%s %s %s" % (old_rev, new_rev, 'refs/heads/master'))

        self.assertEqual(p.returncode, 102, err)

    def test_pass_push(self):
        new_rev = self.__repo.parse_rev('HEAD')
        old_rev = self.__repo.parse_rev('HEAD~2')

        command = 'python %s --binary-check' % self.__script_path

        p = Popen(['bash', '-c', command], cwd=self.__test_repo_dir, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate("%s %s %s" % (old_rev, new_rev, 'refs/heads/master'))

        self.assertEqual(p.returncode, 0, err)

    def test_disabled_check(self):
        new_rev = self.__repo.parse_rev('HEAD')
        old_rev = self.__repo.parse_rev('HEAD~1')

        command = 'python %s' % self.__script_path

        p = Popen(['bash', '-c', command], cwd=self.__test_repo_dir, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate("%s %s %s" % (old_rev, new_rev, 'refs/heads/master'))

        self.assertEqual(p.returncode, 0, err)
