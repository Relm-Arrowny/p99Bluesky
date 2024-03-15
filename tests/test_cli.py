import subprocess
import sys

from p99Bluesky import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "p99Bluesky", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
