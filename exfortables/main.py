import numpy as np
from talys_class import Talys

# Initialize instance
t = Talys()
# targets = [
#     ["Zr", 90, 40], ["Zr", 91, 40], ["Zr", 92, 40], ["Zr", 94, 40], ["Zr", 96, 40],
#     ["Nb", 93, 41],
#     ["Mo", 92, 42], ["Mo", 94, 42], ["Mo", 95, 42], ["Mo", 96, 42], ["Mo", 97, 42], ["Mo", 98, 42], ["Mo", 100, 42],
#     ["Rh", 103, 45],
#     ["Pd", 105, 46], ["Pd", 106, 46],["Pd", 110, 46],
#     ["Ag", 107, 47], ["Ag", 109, 47],
#     ["In", 115, 49],
#     ["Sn", 112, 50], ["Sn", 114, 50],["Sn", 116, 50], ["Sn", 117, 50], ["Sn", 118, 50], ["Sn", 119, 50], ["Sn", 120, 50], ["Sn", 122, 50], 
#     ["Sn", 124, 50],
#     ["Sb", 121, 51], ["Sb", 123, 51],
#     ["Te", 120, 52],
#     ["I", 127, 53],["I", 129, 53],
#     ["Cs", 133, 55],
#     ["Ba", 130, 56], ["Ba", 132, 56],["Ba", 136, 56], ["Ba", 137, 56], ["Ba", 138, 56],
#     ["La", 139, 57],
#     ["Ce", 136, 58], ["Ce", 140, 58], ["Ce", 142, 58],
#     ["Nd", 142, 60], ["Nd", 143, 60], ["Nd", 144, 60], ["Nd", 145, 60], ["Nd", 146, 60], ["Nd", 148, 60], ["Nd", 150, 60]
# ]

targets = [["Zr", 90, 40]]

for target in targets:
    symbol, A, Z = target

    residualA = A - 1
    residual_file = f"rp{str(Z).zfill(3)}{str(residualA).zfill(3)}.tot"

    for ld in range(1, 4):
        filename = f"{symbol}{A}ld{ld}"
        # Generate input
        t.write_input(target, "g", "n", ld)

        # Run TALYS
        t.run(target, filename)

        # Read residual cross section
        output_dir = t.output_dir / f"{symbol}-{A}"
        df = t.read_yandf(output_dir / residual_file)
        df.columns = ["Energy(MeV)", "Cross_Section(mb)"]
        # Save t.run dataframe to output folder
        df.to_csv(output_dir / f"{residual_file}_ld{ld}.csv",index=False)
        print(f"Completed {symbol}-{A}, LD{ld}")

        # Delete all files except CSV files
        for item in output_dir.iterdir():
            if item.is_file() and item.suffix.lower() != ".csv":
                item.unlink()

