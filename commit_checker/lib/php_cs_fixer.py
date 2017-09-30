import os
import subprocess
import sys

from git_repository import GitRepository
from tmp_directory import TmpDirectory


class PhpCsFixer:
    def __init__(self, repo, php_cs_fixer_executable, path_to_config_file=".php_cs"):
        assert isinstance(repo, GitRepository)
        self.__repo = repo
        self.__path_to_php_cs_fixer_executable = php_cs_fixer_executable
        self.__path_to_config_file = path_to_config_file

    def check_push(self, old_rev, new_rev):
        directory_for_check = TmpDirectory.create_tmp_dir()

        files_to_check = self.__repo.get_changed_file_names(old_rev, new_rev)

        files_to_check += [self.__path_to_config_file]

        for file_path in files_to_check:
            file_hash = self.__repo.get_object_hash_by_commit_and_path(new_rev, file_path)
            self.__repo.create_file_by_object_hash(file_hash, file_path, directory_for_check)

        # todo: get dirs to create automatically
        dirs_to_create = ['app', 'scr', 'tests']

        for dir_path in dirs_to_create:
            full_directory_path = os.path.join(directory_for_check, dir_path)
            if not os.path.isdir(full_directory_path):
                os.makedirs(full_directory_path)

        php_cs_fixer_command = "%s fix -v --dry-run --config %s" % (
            self.__path_to_php_cs_fixer_executable,
            self.__path_to_config_file
        )

        dev_null = open(os.devnull, 'w')
        return_code = subprocess.call(['bash', '-c', php_cs_fixer_command], cwd=directory_for_check, stderr=dev_null)
        if return_code != 0:
            return_code += 100
            sys.stderr.write("return code: %s" % return_code)

            exit(return_code)
