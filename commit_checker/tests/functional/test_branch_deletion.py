import os
import unittest
from subprocess import Popen, PIPE

from commit_checker.lib import TmpDirectory
from commit_checker.tests.support import GitRepo


class FunctionalTestBranchDeletion(unittest.TestCase):
    def setUp(self):
        self.__test_repo_dir = TmpDirectory.create_tmp_dir()
        self.__repo = GitRepo(self.__test_repo_dir)
        self.__script_path = os.path.abspath(os.path.dirname(__file__) + '/../../')

    def test_branch_deletion(self):
        new_rev = self.__repo.parse_rev('0000000000000000000000000000000000000000')
        old_rev = self.__repo.parse_rev('HEAD')

        command = 'python %s' % self.__script_path

        p = Popen(['bash', '-c', command], cwd=self.__test_repo_dir, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate("%s %s %s" % (old_rev, new_rev, 'refs/heads/master'))

        self.assertEqual(p.returncode, 0, err)
