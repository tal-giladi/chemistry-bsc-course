"""Download a structure from the Protein Data Bank (RCSB) into data/downloaded/.

Run:   py fetch_pdb.py 4CHA
       py fetch_pdb.py 4CHA 1CHO
PDB archive files are CC0 (public domain); data/downloaded/ is ignored by git, so the files stay
on your computer only. Large structures have no legacy .pdb file; pick another entry if the
download fails with "not found".
"""
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "downloaded"


def fetch(pdb_id):
    pdb_id = pdb_id.strip().upper()
    if len(pdb_id) != 4 or not pdb_id.isalnum():
        raise ValueError(f"{pdb_id!r} is not a 4-character PDB ID")
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / f"{pdb_id}.pdb"
    if target.exists():
        print(f"{target.relative_to(HERE)} already exists")
        return target
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{pdb_id}: not found ({e.code}) at {url}")
    target.write_bytes(data)
    print(f"saved {target.relative_to(HERE)} ({len(data) / 1024:.0f} KB)")
    return target


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
    for arg in sys.argv[1:]:
        fetch(arg)
