import numpy as np
from talys_class import Talys

# Initialize instance
t = Talys()
targets = [["Zr", 90, 40], ["Zr", 91, 40], ["Zr", 92, 40], ["Zr", 94, 40], ["Zr", 96, 40]]


for target in targets:
    symbol, A, Z = target

    residualA = A - 1
    residual_file = f"rp{str(Z).zfill(3)}{str(residualA).zfill(3)}.tot"

    for ld in range(1, 4):
        filename = f"{symbol}{A}ld{ld}"

        # Generate input
        t.write_input(target, "g", "n", ld)