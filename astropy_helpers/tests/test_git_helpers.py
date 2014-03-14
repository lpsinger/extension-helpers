import imp
import os
import re

from setuptools.sandbox import run_setup

from . import *


_DEV_VERSION_RE = re.compile(r'\d+\.\d+(?:\.\d+)?\.dev(\d+)')


def test_update_git_devstr(testpackage, capsys):
    """Tests that the commit number in the package's version string updates
    after git commits even without re-running setup.py.
    """

    run_setup('setup.py', ['--version'])

    stdout, stderr = capsys.readouterr()
    version = stdout.strip()

    m = _DEV_VERSION_RE.match(version)
    assert m

    revcount = int(m.group(1))

    import packagename
    assert packagename.__version__ == version

    # Make a silly git commit
    with open('.test', 'w'):
        pass

    run_cmd('git', ['add', '.test'])
    run_cmd('git', ['commit', '-m', 'test'])

    import packagename.version
    imp.reload(packagename.version)
    imp.reload(packagename)

    m = _DEV_VERSION_RE.match(packagename.__version__)
    assert m
    assert int(m.group(1)) == revcount + 1
