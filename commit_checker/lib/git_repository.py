import os
import subprocess


class GitRepository:
    def __init__(self, repo_dir):
        assert os.path.isdir(repo_dir)
        self.__repo_dir = repo_dir

    @staticmethod
    def is_revision_empty(rev):
        return rev == "0000000000000000000000000000000000000000"

    def get_default_branch_name(self):
        command = 'git rev-parse --abbrev-ref HEAD'
        return subprocess.check_output(['bash', '-c', command], cwd=self.__repo_dir).split("\n")[0]

    def get_changed_file_names(self, old_rev, new_rev):
        bash_command = "git diff --name-only --diff-filter=ACMRT {} {}".format(old_rev, new_rev)

        return subprocess.check_output(['bash', '-c', bash_command], cwd=self.__repo_dir).split("\n")[:-1]

    def get_object_hash_by_commit_and_path(self, commit_hash, relative_file_path):
        bash_command = "git ls-tree --full-name -r %s | egrep \"(\s)%s\$\" | awk '{ print $3 }'" % (
            commit_hash, relative_file_path)

        return subprocess.check_output(['bash', '-c', bash_command], cwd=self.__repo_dir).split("\n")[0]

    def create_file_by_object_hash(self, object_hash, file_path, destination_dir):
        assert os.path.isdir(destination_dir)

        file_dir_name = os.path.dirname(file_path)
        full_directory_path = os.path.join(destination_dir, file_dir_name)

        if not os.path.isdir(full_directory_path):
            os.makedirs(full_directory_path)

        bash_command = "git cat-file blob %s > %s" % (object_hash, os.path.join(destination_dir, file_path))
        if subprocess.check_call(['bash', '-c', bash_command], cwd=self.__repo_dir) != 0:
            raise RuntimeError('error while checking files')

    def get_commit_list(self, old_rev, new_rev):
        bash_command = "git log {}..{} --format=%H --reverse".format(old_rev, new_rev)

        return subprocess.check_output(['bash', '-c', bash_command], cwd=self.__repo_dir).split("\n")[:-1]
