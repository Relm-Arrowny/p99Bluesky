import subprocess
import time

p = subprocess.Popen(
    ["python", "/workspaces/p99-bluesky/tests/junk.py"],
    stdin=subprocess.PIPE,
    stderr=subprocess.PIPE,
    stdout=subprocess.PIPE,
)

time.sleep(1)

p.terminate()
