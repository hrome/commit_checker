import os
import sys

from lib import GitRepository
from lib import PhpCsFixer


def main(args):
    repo = GitRepository(os.path.curdir)
    fixer = PhpCsFixer(repo, '/usr/local/bin/php-cs-fixer-v2')
    old_rev, new_rev, ref_name = sys.stdin.readline().split(' ')

    if old_rev == "0000000000" + "0000000000" + "0000000000" + "0000000000":
        old_rev = repo.get_default_branch_name()

    if new_rev == "00000000000" + "000000000" + "0000000000" + "0000000000":
        raise RuntimeError

    fixer.check_push(old_rev, new_rev)
    pass


if __name__ == '__main__':
    main(sys.argv)
