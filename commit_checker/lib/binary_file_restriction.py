# -*- coding: utf-8 -*-
import os
import subprocess

from checker_interface import CheckerInterface
from tmp_directory import TmpDirectory


class BinaryFileRestriction(CheckerInterface):
    def __init__(self):
        self.file_for_binary_check_name = 'file_for_binary_check'
        self.error_exit_code = 102

    def check(self, file_path, object_hash):
        tmp_dir = TmpDirectory.create_tmp_dir()

        bash_command = "git cat-file blob {} > {}/{}".format(
            object_hash, tmp_dir, self.file_for_binary_check_name)
        if subprocess.check_call(['bash', '-c', bash_command]) != 0:
            print "error while checking files out"
            exit(1)

        if self.is_file_binary(os.path.join(tmp_dir, self.file_for_binary_check_name)):
            self.print_error(file_path, object_hash)
            exit(self.error_exit_code)

    @staticmethod
    def is_file_binary(file_path):
        text_chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})

        chunk = open(file_path, 'rb').read(1024)

        return bool(chunk.translate(None, text_chars))

    @staticmethod
    def print_error(file_name, commit):
        print "file {} in commit {} seems to be binary file".format(file_name, commit)
        print '''
        00000000  89 50 4e 47 0d 0a 1a 0a  00 00 00 0d 49 48 44 52  |.PNG........IHDR|
        00000010  00 00 00 87 00 00 00 a0  08 03 00 00 00 11 90 8f  |................|
        00000020  b6 00 00 00 04 67 41 4d  41 00 00 d6 d8 d4 4f 58  |.....gAMA.....OX|
        00000030  32 00 00 00 19 74 45 58  74 53 6f 66 74 77 61 72  |2....tEXtSoftwar|
        00000040  65 00 41 64 6f 62 65 20  49 6d 61 67 65 52 65 61  |e.Adobe ImageRea|
        00000050  64 79 71 c9 65 3c 00 00  03 00 50 4c 54 45 22 22  |dyq.e<....PLTE""|
        00000060  22 56 56 56 47 47 47 33  33 33 30 30 30 42 42 42  |"VVVGGG333000BBB|
        00000070  4b 4b 4b 40 40 40 15 15  15 4f 4f 4f 2c 2c 2c 3c  |KKK@@@...OOO,,,<|
        00000080  3c 3c 3e 3e 3e 3a 39 39  04 04 04 1d 1d 1d 35 35  |<<>>>:99......55|
        00000090  35 51 50 50 37 37 37 11  11 11 25 25 25 0d 0d 0d  |5QPP777...%%%...|
        000000a0  27 27 27 1a 1a 1a 38 38  38 2a 2a 2a 08 08 08 20  |''....888**...  |
        000000b0  20 20 17 17 17 2e 2e 2e  13 13 13 bb bb bb 88 88  |  ..............|
        '''
