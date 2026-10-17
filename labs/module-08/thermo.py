"""Shared helper for the Module 8 labs: read thermo_data.csv into a dictionary.

Each row: species, dHf (kJ/mol), dGf (kJ/mol), S (J/(mol K)), molar mass (g/mol), source.
Values: OpenStax Chemistry 2e, Appendix G (298.15 K, 1 bar), checked 2026-10-16;
NaHCO3(s) dHf from the NBS tables as quoted on Wikipedia (no dGf or S given here).
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_table(path=HERE / "thermo_data.csv"):
    table = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            table[row["species"]] = {
                k: (float(row[k]) if row[k] else None)
                for k in ("dHf_kJ_mol", "dGf_kJ_mol", "S_J_molK", "M_g_mol")
            }
    return table
