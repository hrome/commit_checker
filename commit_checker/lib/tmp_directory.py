import atexit
import os
import shutil
import signal
import tempfile


class TmpDirectory:
    __created_tmp_dirs = []
    __handlers_registered = False

    def __init__(self):
        pass

    @classmethod
    def create_tmp_dir(cls):
        if not cls.__handlers_registered:
            cls.__register_handlers()

        tmp_dir = tempfile.mkdtemp()
        cls.__created_tmp_dirs.append(tmp_dir)

        return tmp_dir

    @classmethod
    def clean_tmp_dirs(cls):
        for dir_path in cls.__created_tmp_dirs:
            if os.path.isdir(dir_path):
                shutil.rmtree(dir_path)

    @classmethod
    def __register_handlers(cls):
        atexit.register(cls.exit_handler)
        signal.signal(signal.SIGQUIT, TmpDirectory.exit_handler)
        signal.signal(signal.SIGINT, TmpDirectory.exit_handler)
        signal.signal(signal.SIGTERM, TmpDirectory.exit_handler)
        cls.__handlers_registered = True

    # noinspection PyUnusedLocal
    @classmethod
    def exit_handler(cls, *args):
        cls.clean_tmp_dirs()
