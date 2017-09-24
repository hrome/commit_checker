import tempfile


class TmpDirectory:
    def __init__(self):
        pass

    @staticmethod
    def create_tmp_dir():
        tmp_dir = tempfile.mkdtemp()

        return tmp_dir
