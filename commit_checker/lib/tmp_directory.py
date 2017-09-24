import os
import shutil
import tempfile


class TmpDirectory:
    __created_tmp_dirs = []

    def __init__(self):
        pass

    @staticmethod
    def create_tmp_dir():
        tmp_dir = tempfile.mkdtemp()
        TmpDirectory.__created_tmp_dirs.append(tmp_dir)

        return tmp_dir

    @staticmethod
    def clean_tmp_dirs():
        for dir_path in TmpDirectory.__created_tmp_dirs:
            if os.path.isdir(dir_path):
                shutil.rmtree(dir_path)
