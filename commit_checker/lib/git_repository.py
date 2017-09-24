import os

import subprocess


class GitRepository:
    def __init__(self, repo_dir):
        assert os.path.isdir(repo_dir)
        self.__repo_dir = repo_dir

    def get_default_branch_name(self):
        command = 'cd %s && git rev-parse --abbrev-ref HEAD' % self.__repo_dir
        return subprocess.check_output(['bash', '-c', command]).split("\n")[0]
