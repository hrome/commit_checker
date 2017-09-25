import os
import subprocess


class GitRepository:
    def __init__(self, repo_dir):
        assert os.path.isdir(repo_dir)
        self.__repo_dir = repo_dir

    def get_default_branch_name(self):
        command = 'git rev-parse --abbrev-ref HEAD'
        return subprocess.check_output(['bash', '-c', command], cwd=self.__repo_dir).split("\n")[0]

    def get_changed_file_names(self, old_rev, new_rev):
        bash_command = "git diff --name-only {} {}".format(old_rev, new_rev)
        return subprocess.check_output(['bash', '-c', bash_command], cwd=self.__repo_dir).split("\n")[:-1]
