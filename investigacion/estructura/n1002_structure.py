#!/usr/bin/env python3
"""Where does p.(Asn1002Lys) sit in BUBR1? Reproduces the structural numbers used in the Track 2 report.

Model: AlphaFold AF-O60566-F1 (human BUBR1, UniProt O60566), model v6 — downloaded if missing.
Definitions (kept explicit so the numbers can be checked):
  - pLDDT: B-factor column of the N1002 C-alpha.
  - burial: heavy atoms within 10 Å of the N1002 C-alpha, counting the residue's own atoms.
  - motifs: HRD-like = H880-G881-D882 ("HGD", catalytic-loop position); DFG-like = D911-F912-S913
    ("DFS", the DxG position that follows the catalytic loop with canonical kinase spacing).
    Distances are C-alpha to C-alpha, from N1002 to the motif's first residue.
Usage: python3 n1002_structure.py
"""
import math, os, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PDB = os.path.join(HERE, "bubr1_af.pdb")
URL = "https://alphafold.ebi.ac.uk/files/AF-O60566-F1-model_v6.pdb"
RES, RADIUS = 1002, 10.0
MOTIFS = {"HRD-like (HGD 880-882)": 880, "DFG-like (DFS 911-913)": 911}
NEIGHBOURS = ["TRP973", "TRP978", "PHE954", "PHE977", "PHE996", "PHE997"]

if not os.path.exists(PDB):                              # the server rejects requests without a User-Agent
    req = urllib.request.Request(URL, headers={"User-Agent": "mva-hackathon-track2/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r, open(PDB, "wb") as fh:
        fh.write(r.read())

atoms = []
for line in open(PDB):
    if line.startswith("ATOM"):
        atoms.append(dict(name=line[12:16].strip(), res=line[17:20], num=int(line[22:26]),
                          xyz=(float(line[30:38]), float(line[38:46]), float(line[46:54])),
                          b=float(line[60:66]), el=line[76:78].strip()))

def dist(a, b):
    return math.dist(a, b)

ca = {a["num"]: a for a in atoms if a["name"] == "CA"}
target = ca[RES]
assert target["res"] == "ASN", f"residue {RES} is {target['res']}, expected ASN"
heavy = [a for a in atoms if a["el"] != "H"]
burial = sum(1 for a in heavy if dist(a["xyz"], target["xyz"]) <= RADIUS)
near = sorted({f"{a['res']}{a['num']}" for a in heavy if a["num"] != RES and dist(a["xyz"], target["xyz"]) <= RADIUS})

print(f"N{RES} pLDDT (C-alpha): {target['b']:.1f}")
print(f"heavy atoms within {RADIUS:.0f} Å of the C-alpha (own atoms included): {burial}")
for label, start in MOTIFS.items():
    print(f"C-alpha distance to {label}: {dist(target['xyz'], ca[start]['xyz']):.1f} Å")
print("aromatic neighbours within 10 Å:", ", ".join(n for n in NEIGHBOURS if n in near))
