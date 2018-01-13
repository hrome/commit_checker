# -*- coding: utf-8 -*-
import subprocess

from checker_interface import CheckerInterface


class FileSizeRestriction(CheckerInterface):
    def __init__(self, max_file_size_in_bytes):
        self.__max_file_size_in_bytes = int(max_file_size_in_bytes)
        self.__error_exit_code = 101

    def check(self, file_path, object_hash):
        bash_command = "git cat-file -s {}".format(object_hash)
        object_size = subprocess.check_output(['bash', '-c', bash_command]).split("\n")[0]
        object_size = int(object_size)

        if object_size > self.__max_file_size_in_bytes:
            self.print_error(file_path, object_hash)
            exit(self.__error_exit_code)

    @staticmethod
    def print_error(file_name, commit):
        print "file {} in commit {} seems to be too large".format(file_name, commit)
        print '''
        ██████╗ ██╗ ██████╗     ███████╗██╗██╗     ███████╗
        ██╔══██╗██║██╔════╝     ██╔════╝██║██║     ██╔════╝
        ██████╔╝██║██║  ███╗    █████╗  ██║██║     █████╗
        ██╔══██╗██║██║   ██║    ██╔══╝  ██║██║     ██╔══╝
        ██████╔╝██║╚██████╔╝    ██║     ██║███████╗███████╗
        ╚═════╝ ╚═╝ ╚═════╝     ╚═╝     ╚═╝╚══════╝╚══════╝
        '''
