from abc import ABCMeta, abstractmethod


class CheckerInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def check(self, file_path, object_hash):
        pass
