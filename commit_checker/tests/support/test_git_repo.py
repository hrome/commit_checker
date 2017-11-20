import os
import shutil
import subprocess


class GitRepo:
    def __init__(self, repo_dir):
        assert os.path.isdir(repo_dir)
        self.__repo_dir = repo_dir
        self.__test_repo_example_dir = os.path.abspath(os.path.dirname(__file__) + '/../_data/repo')
        self.init_test_repo()

    def init_test_repo(self):
        pass
        shutil.rmtree(self.__repo_dir)
        shutil.copytree(self.__test_repo_example_dir, self.__repo_dir)
        command_list = [
            'git init',
            'git add .php_cs',
            'git commit -m "Initial commit"',
            'git add binary.dat',
            'git commit -m "Add binary file"',
            'git add src/pass.php',
            'git commit -m "Add file"',
            'git add src/reject.php',
            'git commit -m "Add file"',
        ]

        dev_null = open(os.devnull, 'w')
        for command in command_list:
            subprocess.check_call(['bash', '-c', command], cwd=self.__repo_dir, stdout=dev_null,
                                  stderr=subprocess.STDOUT)

    def parse_rev(self, rev):
        command = 'git rev-parse %s' % rev
        return subprocess.check_output(['bash', '-c', command], cwd=self.__repo_dir).split("\n")[0]
