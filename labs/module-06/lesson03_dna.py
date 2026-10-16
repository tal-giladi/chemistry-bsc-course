"""Lesson 06.3 hands-on: from a DNA sequence to a protein, primer melting
temperatures, and how much DNA fits in a cell.

Fill in the four TODO functions, then run:
       py lesson03_dna.py                     (designed ubiquitin gene)
       py lesson03_dna.py my_sequence.fasta   (any coding sequence, starting at ATG)
Reference solution: lesson03_dna_solution.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# The standard genetic code, codons in TCAG order: TTT, TTC, TTA, TTG, TCT, ... GGG.
# '*' marks a stop codon.
BASES = "TCAG"
AMINO = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
CODON_TABLE = {a + b + c: AMINO[16 * i + 4 * j + k]
               for i, a in enumerate(BASES) for j, b in enumerate(BASES) for k, c in enumerate(BASES)}

UNIPROT_UBIQUITIN = "MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG"
RISE_NM = 0.34          # rise per base pair in B-DNA (OpenStax Biology 2e, 14.2)
BP_MASS = 650.0         # g/mol, average mass of one base pair (sodium salt), approximate
NA = 6.02214076e23      # 1/mol, CODATA 2022 (exact)


def read_fasta(path):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    return "".join(l.strip() for l in lines if l and not l.startswith(">")).upper()


def reverse_complement(seq):
    """The other strand, read 5' to 3': complement each base (A-T, G-C) and reverse the order.
    TODO: a dict {"A": "T", ...} and reversed(seq)."""
    return None


def gc_content(seq):
    """Fraction of bases that are G or C.
    TODO: use seq.count()."""
    return None


def wallace_tm(primer):
    """Rough melting temperature (C) of a short oligonucleotide: Tm = 2 (A + T) + 4 (G + C).
    A first estimate only, for primers of about 20 bases or fewer.
    TODO: count A+T and G+C."""
    return None


def translate(cds):
    """Translate a coding sequence codon by codon from the first base, stopping at the first stop
    codon (not included). Returns the one-letter protein sequence.
    TODO: step through the sequence 3 bases at a time with CODON_TABLE; stop at '*'."""
    return None


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "ubiquitin_designed.fasta"
    cds = read_fasta(path)
    if None in (reverse_complement("ATG"), gc_content("ATG"), wallace_tm("ATG"), translate("ATGTAA")):
        print("TODO: write reverse_complement(), gc_content(), wallace_tm() and translate() first.")
        return
    print(f"{path.name}: {len(cds)} bases, GC content {gc_content(cds):.1%}")
    prot = translate(cds)
    print(f"protein ({len(prot)} residues): {prot}")
    if path.name == "ubiquitin_designed.fasta":
        print(f"identical to UniProt P0CG48 residues 1-76: {prot == UNIPROT_UBIQUITIN}")

    fwd = cds[:20]
    rev = reverse_complement(cds[-20:])
    for name, p in (("forward primer", fwd), ("reverse primer", rev)):
        print(f"{name}: 5'-{p}-3'  GC {gc_content(p):.0%}  Wallace Tm {wallace_tm(p)} C")

    # point mutations at codon 48 (Lys48, the residue that links ubiquitin chains)
    i = 47 * 3
    codon = cds[i:i + 3]
    for new in ("AGG", "TAG"):
        mut = cds[:i] + new + cds[i + 3:]
        p = translate(mut)
        print(f"codon 48 {codon} -> {new}: protein length {len(p)}, residue 48 = {p[47] if len(p) > 47 else 'none (stop)'}")

    # one human genome copy in numbers
    bp = 3.1e9
    print(f"\nhuman genome, one copy of about {bp:.1e} bp:")
    print(f"  length {bp * RISE_NM * 1e-9:.2f} m, mass {bp * BP_MASS / NA * 1e12:.1f} pg, information {2 * bp / 8 / 1e6:.0f} MB")


if __name__ == "__main__":
    main()
