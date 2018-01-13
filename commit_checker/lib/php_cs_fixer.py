import os
import sys
from subprocess import Popen, PIPE

from git_repository import GitRepository
from tmp_directory import TmpDirectory


class PhpCsFixer:
    def __init__(self, repo, php_cs_fixer_executable, path_to_config_file, dirs_to_create):
        assert isinstance(repo, GitRepository)
        self.__repo = repo
        self.__path_to_php_cs_fixer_executable = php_cs_fixer_executable
        self.__path_to_config_file = path_to_config_file
        self.__dirs_to_create = dirs_to_create

    def check_push(self, old_rev, new_rev):
        directory_for_check = TmpDirectory.create_tmp_dir()

        files_to_check = self.__repo.get_changed_file_names(old_rev, new_rev)

        files_to_check += [self.__path_to_config_file]

        for file_path in files_to_check:
            file_hash = self.__repo.get_object_hash_by_commit_and_path(new_rev, file_path)
            self.__repo.create_file_by_object_hash(file_hash, file_path, directory_for_check)

        for dir_path in self.__dirs_to_create:
            full_directory_path = os.path.join(directory_for_check, dir_path)
            if not os.path.isdir(full_directory_path):
                os.makedirs(full_directory_path)

        php_cs_fixer_command = "%s fix -v --dry-run --config %s" % (
            self.__path_to_php_cs_fixer_executable,
            self.__path_to_config_file
        )

        p = Popen(['bash', '-c', php_cs_fixer_command], cwd=directory_for_check, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()

        return_code = p.returncode

        if return_code != 0:
            program_return_code = 100 + return_code
            sys.stderr.write(err)
            sys.stderr.write(output)
            sys.stderr.write("exit code: %s\n" % return_code)
            sys.stderr.write("see https://github.com/FriendsOfPHP/PHP-CS-Fixer#exit-codes\n")

            exit(program_return_code)
