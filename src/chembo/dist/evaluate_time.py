"""
Evaluate runtime of OT-distance computation on ChEMBL molecules.
"""
from datasets.loaders import get_chembl
from dist.ot_dist_computer import OTChemDistanceComputer

from collections import defaultdict
from time import time
import numpy as np

def test(N=100):
    dist_computer = OTChemDistanceComputer()
    mols = get_chembl(max_size=N, as_mols=True)
    natoms = [mol.to_rdkit().GetNumAtoms() for mol in mols]
    times = defaultdict(list)
    for i in range(N):
        for j in range(i):
            t0 = time()
            dist_computer([mols[i].to_smiles()], [mols[j].to_smiles()])
            time_elapsed = time() - t0
            times[natoms[i] + natoms[j]].append(time_elapsed)
    for k, res_lst in times.items():
        times[k] = np.mean(res_lst)
    return times


if __name__ == "__main__":
    times = test(500)
    print(times)
