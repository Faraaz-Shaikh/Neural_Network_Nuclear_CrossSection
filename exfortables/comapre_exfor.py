import numpy as np
import pandas as pd
from pathlib import Path
import subprocess


class Talys():
    def __init__(self):
       #Define talys , exfortables paths and folder to store the input-output files
       self.talys_dir = Path("/run/media/faraaz/Data_faru_lnx/software/talys_tars/talys/bin/talys")
       self.exfortables_dir = Path("/run/media/faraaz/Data_faru_lnx/software/exfortables_py")
       self.working_dir = Path("/run/media/faraaz/Data_faru_lnx/talys")
       self.input_dir = Path("/run/media/faraaz/Data_faru_lnx/talys/input")
       self.output_dir = Path("/run/media/faraaz/Data_faru_lnx/talys/output")

    def read_yandf(self, path):
        df = pd.read_csv(path, sep=r"\s+" , comment="#", header = None)
        return df

    def fetch_exfortables(self, target,targetA, proj, ejec):
        symbol = target
        exfor_path = Path(f"{self.exfortables_dir}/{proj}/{symbol}-{targetA}/{proj}-{ejec}/xs")
        exfor_df = pd.DataFrame()
        exfor_files = [f for f in exfor_path.iterdir() if f.is_file()]
        for f in exfor_files:
            print(f"file : {f}")
            df = self.read_yandf(path=f)
            exfor_df = pd.concat([exfor_df, df], ignore_index=True)
        
        exfor_df = (
            exfor_df.sort_values(by=0, ascending=True)
            .drop_duplicates(subset=[0], keep='first')
            .reset_index(drop=True)
        )
        exfor_df[2] = exfor_df[2]*1000
        exfor_df[3] = exfor_df[3]*1000
        return exfor_df

    def write_input(self, target, proj, ejec ,ldmodel):
        self.symbol = target[0]
        self.A = int(target[1])
        self.Z = int(target[2])
    
        #define folder and output folders for talys
        input_dir = f"{self.input_dir}/{self.symbol}"
        Path(input_dir).mkdir(parents=True, exist_ok=True)

        output_dir =  f"{self.output_dir}/{self.symbol}"
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        # self.output_dir =  f"{self.working_dir}/output/{self.symbol}"
        # Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        exfortables_df = self.fetch_exfortables(target = self.symbol, targetA = self.A, proj= proj, ejec=ejec)
        exfortables_df.to_csv(f"{output_dir}/{self.symbol}{self.A}x4.csv")
        
        energy = exfortables_df[0].to_numpy().astype(float)
        np.savetxt(f"{input_dir}/energies", energy, delimiter="", newline = "\n", fmt="%.4f")
        with open(f"{input_dir}/{self.symbol}{self.A}ld{ldmodel}.inp", "w") as f:
            if ldmodel!=3:
                print(f"writing to {f.name}")
                f.write(f"projectile {proj}\n")
                f.write(f"element {self.symbol}\n")
                f.write(f"mass {self.A}\n")
                f.write(f"energy {input_dir}/energies\n")
                f.write(f"ldmodel {int(ldmodel)}\n")
                print(f"file created: {f.name}")
            elif ldmodel == 3:
                print(f"writing to {f.name}")
                f.write(f"projectile {proj}\n")
                f.write(f"element {self.symbol}\n")
                f.write(f"mass {self.A}\n")
                f.write(f"energy {input_dir}/energies\n")
                f.write(f"legacy y\n")
                f.write(f"ldmodel {int(ldmodel)}\n")
                print(f"file created: {f.name}")


    def run(self,target, filename):
        symbol = target[0]

        input_dir = self.input_dir / symbol
        output_dir = self.output_dir / symbol
        print(output_dir)
        cmd = f"talys <{input_dir}/{filename}.inp> {output_dir}/{filename}.out"
        print(cmd)
        subprocess.run(cmd, shell=True, check=True, cwd=str(output_dir))




# Initialize instance
t = Talys()
targets = [
    ["Zr", 90, 40], ["Zr", 91, 40], ["Zr", 92, 40], ["Zr", 94, 40], ["Zr", 96, 40],
    ["Nb", 93, 41],
    ["Mo", 92, 42], ["Mo", 94, 42], ["Mo", 95, 42], ["Mo", 96, 42], ["Mo", 97, 42], ["Mo", 98, 42], ["Mo", 100, 42],
    ["Rh", 103, 45],
    ["Pd", 105, 46], ["Pd", 106, 46],["Pd", 110, 46]
    ["Ag", 107, 47], ["Ag", 109, 47],
    ["In", 115, 49],
    ["Sn", 112, 50], ["Sn", 114, 50],["Sn", 116, 50], ["Sn", 117, 50], ["Sn", 118, 50], ["Sn", 119, 50], ["Sn", 120, 50], ["Sn", 122, 50], 
    ["Sn", 124, 50],
    ["Sb", 121, 51], ["Sb", 123, 51],
    ["Te", 120, 52],
    ["I", 127, 53],["I", 129, 53],
    ["Cs", 133, 55],
    ["Ba", 130, 56], ["Ba", 132, 56],["Ba", 136, 56], ["Ba", 137, 56], ["Ba", 138, 56],
    ["La", 139, 57],
    ["Ce", 136, 58], ["Ce", 140, 58], ["Ce", 142, 58],
    ["Nd", 142, 60], ["Nd", 143, 60], ["Nd", 144, 60], ["Nd", 145, 60], ["Nd", 146, 60], ["Nd", 148, 60], ["Nd", 150, 60],
]
df_targets = pd.DataFrame(targets, columns=["Symbol", "A", "Z"])
t = Talys()
#Iterate and pass the symbol as target (e.g. t.run(target="Ba"), t.run(target="W"), etc.)
for target in targets:
        A = str(target[1]).zfill(3)
        Z = str(target[2]).zfill(3)
        residual_file = f"rp{Z}{A}.tot"
        print(residual_file)
        
        for ld in range(1,3,1):
            filename = f"{target[0]}{target[1]}ld{ld}"
        
            t.run(target, filename)

            output_dir = t.output_dir / target[0]
            print(t.output_dir)
            residual_df = t.read_yandf(output_dir / residual_file)
            residual_df.to_csv(f"{output_dir}/rp{Z}{A}ld{ld}.csv")




