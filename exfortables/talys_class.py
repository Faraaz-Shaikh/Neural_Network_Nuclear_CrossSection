import numpy as np
import pandas as pd
from pathlib import Path
import subprocess

class Talys():
    def __init__(self):
       #Define talys , exfortables paths and folder to store the input-output files
       #self.talys_dir = Path("/run/media/faraaz/Data_faru_lnx/software/talys_tars/talys/bin/talys")
       self.exfortables_dir = Path("/run/media/faraaz/Data_faru_lnx/software/exfortables_py")
       self.working_dir = Path("/run/media/faraaz/Data_faru_lnx/talys")
       self.input_dir = Path("/run/media/faraaz/Data_faru_lnx/talys/input")
       self.output_dir = Path("/run/media/faraaz/Data_faru_lnx/talys/output")

    def x4_info(self, exfor_files):
        exfor_df = pd.DataFrame()
        for exfor_file in exfor_files:
            with open(exfor_file, "r") as txt:
                data = txt.read()
                _, _, after = data.partition("Residual: ")
                _, _, nuclide = after.partition("Nuclide: ")
                nuclide = nuclide.splitlines()[0]
                _, _, author = after.partition("First author: ")
                author = author.splitlines()[0]
                _, _, year = after.partition("Year: ")
                year = year.splitlines()[0]
                print(f"target: {nuclide}, year: {year}")
                if "M" not in nuclide:
                    data = pd.read_csv(exfor_file, comment="#",sep="\s+" , names = ["Energy(MeV)", "dE", "Cross_Section(Barns)", "dcs"])
                    data['author'] = author 
                    data["nuclide"] = nuclide 
                    data['year'] = year
                    exfor_df = pd.concat([exfor_df,data], ignore_index=True)
        return exfor_df

    def read_yandf(self, path):
        df = pd.read_csv(path, sep=r"\s+" , comment="#", header = None)
        return df

    # def fetch_exfortables(self, target,targetA, proj, ejec):
    #     symbol = target
    #     exfor_path = Path(f"{self.exfortables_dir}/{proj}/{symbol}-{targetA}/{proj}-{ejec}/xs")
    #     exfor_df = pd.DataFrame()
    #     exfor_files = [f for f in exfor_path.iterdir() if f.is_file()]
    #     for f in exfor_files:
    #         print(f"file : {f}")
    #         df = self.read_yandf(path=f)
    #         exfor_df = pd.concat([exfor_df, df], ignore_index=True)
        
    #     exfor_df = (
    #         exfor_df.sort_values(by=0, ascending=True)
    #         .drop_duplicates(subset=[0], keep='first')
    #         .reset_index(drop=True)
    #     )
    #     exfor_df[2] = exfor_df[2]*1000
    #     exfor_df[3] = exfor_df[3]*1000
    #     return exfor_df

    def write_input(self, target, proj, ejec ,ldmodel):
        symbol = target[0]
        A = int(target[1])
        Z = int(target[2])
        exfortables_dir  = Path(f"{self.exfortables_dir}/{proj}/{target[0]}-{target[1]}/{proj}-{ejec}/xs")
        exfor_files = [f for f in exfortables_dir.iterdir() if f.is_file()]
        #define folder and output folders for talys
        input_dir = f"{self.input_dir}/{symbol}-{A}"
        Path(input_dir).mkdir(parents=True, exist_ok=True)

        output_dir =  f"{self.output_dir}/{symbol}-{A}"
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        # output_dir =  f"{self.working_dir}/output/{symbol}"
        # Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        # exfortables_df = self.fetch_exfortables(target = self.symbol, targetA = self.A, proj= proj, ejec=ejec)
        # exfortables_df.to_csv(f"{output_dir}/{self.symbol}{self.A}x4.csv")
        
        # energy = exfortables_df[0].to_numpy().astype(float)
        # energy = energy[energy < 40.0]
        # energy_file = Path(f"{input_dir}/energies")

        # if not energy_file.exists():
        #     np.savetxt(energy_file, energy, fmt="%.4f")
        exfortables_df = self.x4_info(exfor_files)
        # energy = exfortables_df["Energy(MeV)"].to_numpy().astype(float)
        # energy = energy[energy < 40.0]
        energy = np.sort(exfortables_df["Energy(MeV)"].unique().astype(float))
        energy = energy[energy < 40.0]
        energy_file = Path(f"{input_dir}/energies")
        np.savetxt(energy_file, energy, fmt="%.4f")
        
        with open(f"{input_dir}/{symbol}{A}ld{ldmodel}.inp", "w") as f:
            if ldmodel!=3:
                print(f"writing to {f.name}")
                f.write(f"projectile {proj}\n")
                f.write(f"element {symbol}\n")
                f.write(f"mass {A}\n")
                f.write(f"energy {input_dir}/energies\n")
                f.write(f"ldmodel {int(ldmodel)}\n")
                print(f"file created: {f.name}")
            elif ldmodel == 3:
                print(f"writing to {f.name}")
                f.write(f"projectile {proj}\n")
                f.write(f"element {symbol}\n")
                f.write(f"mass {A}\n")
                f.write(f"energy {input_dir}/energies\n")
                f.write(f"legacy y\n")
                f.write(f"ldmodel {int(ldmodel)}\n")
                print(f"file created: {f.name}")


    def run(self,target, filename):
        symbol = target[0]
        A = target[1]
        folder_name = f"{symbol}-{A}"
        input_dir = self.input_dir / folder_name
        output_dir = self.output_dir / folder_name
        print(output_dir)
        cmd = f"talys <{input_dir}/{filename}.inp> {output_dir}/{filename}.out"
        print(cmd)
        subprocess.run(cmd, shell=True, check=True, cwd=str(output_dir))