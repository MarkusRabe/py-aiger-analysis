#!/usr/bin/env python

import contextlib
import os
from subprocess import check_call
import tarfile
import zipfile
from pathlib import Path

GET_ABC_CMD = "wget https://github.com/berkeley-abc/abc/archive/master.zip"
GET_AIGER_CMD = "wget http://fmv.jku.at/aiger/aiger-1.9.9.tar.gz"
GET_CADET_CMD = "wget https://github.com/MarkusRabe/cadet/archive/v2.5.tar.gz"


# https://stackoverflow.com/questions/41742317/how-can-i-change-directory-with-python-pathlib
@contextlib.contextmanager
def working_directory(path):
    """Changes working directory and returns to previous on exit."""
    prev_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def install_aiger():
    aiger_path = Path(os.environ['HOME']) / ".cache" / "aiger"
    print("Installing AIGER.")
    if not aiger_path.exists():
        aiger_path.mkdir()
    elif (aiger_path / "aiger-1.9.9").exists():
        print("Using cached version.")
        return

    with working_directory(aiger_path):
        check_call(GET_AIGER_CMD, shell=True)
        print("Unzipping AIGER")
        with tarfile.open("aiger-1.9.9.tar.gz") as f:
            f.extractall()

    with working_directory(aiger_path / "aiger-1.9.9"):
        check_call("./configure.sh && make", shell=True)


def install_abc():
    abc_path = Path(os.environ["HOME"]) / ".cache" / "abc"
    print("Installing ABC.")
    if not abc_path.exists():
        abc_path.mkdir()
    elif (abc_path / "abc-master").exists():
        print("Using cached version.")
        return

    with working_directory(abc_path):
        check_call(GET_ABC_CMD, shell=True)

        print("Unzipping ABC")
        with zipfile.ZipFile(abc_path / "master.zip", "r") as f:
            f.extractall()

    with working_directory(abc_path / 'abc-master'):
        check_call("cmake . && make", shell=True)


def install_cadet():
    cadet_path = Path(os.environ['HOME']) / ".cache" / "cadet"
    print("Installing CADET.")
    if not cadet_path.exists():
        cadet_path.mkdir()
    elif (cadet_path / "cadet").exists():
        print("Using cached version.")
        return

    with working_directory(cadet_path):
        check_call(GET_CADET_CMD, shell=True)

        print("Unzipping CADET")
        with tarfile.open("v2.5.tar.gz") as f:
            f.extractall()

    assert (cadet_path / "cadet-2.5").exists()
    with working_directory(cadet_path / "cadet-2.5"):
        check_call("./configure && make", shell=True)


def main():
    install_abc()
    install_aiger()
    install_cadet()


if __name__ == '__main__':
    main()
