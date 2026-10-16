"""Lesson 05.1: check that your Python and packages match the course pins.

It reads labs/common/requirements.txt, compares each pinned version with what is installed in the
Python that runs this script, and prints one line per package. Run it with the Python inside
your virtual environment (from the repo root):

    .venv\\Scripts\\python labs/module-05/check_setup.py        (Windows)
    .venv/bin/python labs/module-05/check_setup.py             (macOS/Linux)

Exit code 0 means everything matches; 1 means something is missing or different.
"""
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

HERE = Path(__file__).resolve().parent
REQUIREMENTS = HERE.parent / "common" / "requirements.txt"
WANTED_PYTHON = (3, 14)


def read_pins(path):
    """Return a dict {package: pinned version} from lines like 'numpy==2.5.4'."""
    pins = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if "==" in line:
            name, ver = line.split("==", 1)
            pins[name.strip()] = ver.strip()
    return pins


def main():
    ok = True
    py = sys.version_info
    in_venv = sys.prefix != sys.base_prefix
    print(f"Python {py.major}.{py.minor}.{py.micro} at {sys.executable}")
    if (py.major, py.minor) != WANTED_PYTHON:
        print(f"  WRONG  the course pins Python {WANTED_PYTHON[0]}.{WANTED_PYTHON[1]}")
        ok = False
    print(f"  virtual environment: {'yes' if in_venv else 'NO - activate .venv or call its python'}")
    if not in_venv:
        ok = False

    pins = read_pins(REQUIREMENTS)
    print(f"\n{len(pins)} pins in {REQUIREMENTS.relative_to(HERE.parent.parent).as_posix()}:")
    for name, wanted in pins.items():
        try:
            have = version(name)
        except PackageNotFoundError:
            print(f"  MISSING  {name:<14} wanted {wanted}")
            ok = False
            continue
        status = "ok     " if have == wanted else "DIFFERS"
        if have != wanted:
            ok = False
        print(f"  {status}  {name:<14} installed {have:<10} pinned {wanted}")

    print("\nAll good: your setup matches the course." if ok else
          "\nFix the lines marked above: pip install -r labs/common/requirements.txt inside the venv.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
