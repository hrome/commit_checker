import os
import subprocess
import unittest

from commit_checker.lib import TmpDirectory
from commit_checker.lib.git_repository import GitRepository


class TestGitRepository(unittest.TestCase):
    def setUp(self):
        self.__repo_dir = TmpDirectory.create_tmp_dir()
        self.__test_file_name = 'test123'
        self.__test_file_content = 'test_content'
        command_list = [
            'git init',
            'git commit --allow-empty -m "Initial commit"',
            'echo 123 > 123',
            'echo %s > %s' % (self.__test_file_content, self.__test_file_name),
            'git add 123 %s' % self.__test_file_name,
            'git commit -m "123 and test"',
            'echo 333 >> 123',
            'git add 123',
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
        self.assertItemsEqual(changed_files, ['123', self.__test_file_name])

    def test_getting_object_hash_by_commit_and_path(self):
        repo = GitRepository(self.__repo_dir)
        command = 'git rev-parse HEAD~1'
        rev = subprocess.check_output(['bash', '-c', command], cwd=self.__repo_dir).split("\n")[0]

        command = 'echo %s | git hash-object --stdin' % self.__test_file_content
        file_hash = subprocess.check_output(['bash', '-c', command], cwd=self.__repo_dir).split("\n")[0]

        file_hash_by_repo = repo.get_object_hash_by_commit_and_path(rev, self.__test_file_name)
        self.assertEqual(file_hash, file_hash_by_repo)

    def test_creating_file_by_object_hash(self):
        repo = GitRepository(self.__repo_dir)
        command = 'echo %s | git hash-object --stdin' % self.__test_file_content
        file_hash = subprocess.check_output(['bash', '-c', command], cwd=self.__repo_dir).split("\n")[0]

        repo.create_file_by_object_hash(file_hash, self.__test_file_name)

        command = 'git hash-object %s' % self.__test_file_name
        file_hash_by_repo = subprocess.check_output(['bash', '-c', command], cwd=self.__repo_dir).split("\n")[0]

        self.assertEqual(file_hash, file_hash_by_repo)

    def test_getting_commit_list(self):
        repo = GitRepository(self.__repo_dir)

        head = subprocess.check_output(['bash', '-c', 'git rev-parse HEAD'], cwd=self.__repo_dir).split("\n")[0]
        head_1 = subprocess.check_output(['bash', '-c', 'git rev-parse HEAD~1'], cwd=self.__repo_dir).split("\n")[0]
        head_2 = subprocess.check_output(['bash', '-c', 'git rev-parse HEAD~2'], cwd=self.__repo_dir).split("\n")[0]

        commit_list = repo.get_commit_list(head_2, head)

        self.assertItemsEqual(commit_list, [head_1, head])
