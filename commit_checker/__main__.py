import os
import sys

from lib import EachCommitChecker
from lib import GitRepository
from lib import Options
from lib import PhpCsFixer


def main(args):
    options = Options()
    config = options.parse(args[1:])
    repo = GitRepository(os.path.curdir)

    old_rev, new_rev, ref_name = sys.stdin.readline().split(' ')

    if repo.is_revision_empty(old_rev):
        old_rev = repo.get_default_branch_name()

    if repo.is_revision_empty(new_rev):
        # case of branch deletion
        exit(0)

    if config.php_cs_fixer_enabled:
        fixer = PhpCsFixer(
            repo,
            config.php_cs_fixer_executable,
            config.php_cs_fixer_config_path,
            config.php_cs_fixer_dirs_to_create
        )
        fixer.check_push(old_rev, new_rev)

    each_commit_checker = EachCommitChecker(config, repo)
    each_commit_checker.check(old_rev, new_rev)


if __name__ == '__main__':
    main(sys.argv)
