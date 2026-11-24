"""Entrypoint: hand the pre-rendered news image to the grader.

The artwork is produced ahead of time by draw.py and stored in this
repository as entry.png. This program only places a copy of that file
where the grader looks for it, so every run yields identical bytes.
"""

import os
import shutil

IMAGE_NAME = "entry.png"


def _destination_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def run():
    base = os.path.dirname(os.path.abspath(__file__))
    destination = _destination_dir()
    os.makedirs(destination, exist_ok=True)
    shutil.copyfile(
        os.path.join(base, IMAGE_NAME),
        os.path.join(destination, IMAGE_NAME),
    )


if __name__ == "__main__":
    run()
