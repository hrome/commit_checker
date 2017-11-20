import subprocess

from binary_file_restriction import BinaryFileRestriction
from checker_interface import CheckerInterface
from git_repository import GitRepository


class EachCommitChecker:
    def __init__(self, config, repo):
        assert isinstance(repo, GitRepository)
        self.__repo = repo
        self.__config = config
        self.__checkers = []
        self.init_checkers()

    def init_checkers(self):
        if self.__config.binary_check_enabled:
            self.__checkers.append(BinaryFileRestriction())
        pass

    def check(self, old_rev, new_rev):
        if not len(self.__checkers):
            return

        commit_list = self.__repo.get_commit_list(old_rev, new_rev)

        previous_commit_hash = old_rev

        for commit_hash in commit_list:
            bash_command = "git diff --name-only {} {}".format(previous_commit_hash, commit_hash)
            files = subprocess.check_output(['bash', '-c', bash_command]).split("\n")[:-1]

            for file_path in files:
                bash_command = "git ls-tree --full-name -r {} | egrep \"(\s){}\$\" | awk '{{ print $3 }}'".format(
                    commit_hash, file_path)
                object_hash = subprocess.check_output(['bash', '-c', bash_command]).split("\n")[0]

                assert object_hash

                for checker in self.__checkers:
                    assert isinstance(checker, CheckerInterface)
                    checker.check(file_path, object_hash)
