from pathlib import Path
from pprint import pprint
import pandas as pd

def x4_info(exfor_files):
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
                data = pd.read_csv(exfor_file, comment="#",sep="\s+" , names = ["Enegy(MeV)", "dE", "Cross_Section(Barns)", "dcs"])
                cols = len(data["dE"])
                data['author'] = [author for i in range(cols)]
                data["nuclide"] = [nuclide for i in range(cols)]
                data['year'] = [year for i in range(cols)]
                exfor_df = pd.concat([exfor_df,data], ignore_index=True)
    return exfor_df


exfortables_dir = Path("/run/media/faraaz/Data_faru_lnx/software/exfortables_py")
text_file = Path("/run/media/faraaz/Data_faru_lnx/software/exfortables_py/g/Zr-90/g-n/xs/Zr-90_g-n_Zr-89_A.Banu-L0248-002-0-2019.txt")
proj = "g"
ejec =  "n"
targets = [["Zr", 90],["Zr",91]]
for target in targets:

    path= Path(f"{exfortables_dir}/{proj}/{target[0]}-{target[1]}/{proj}-{ejec}/xs")
    print(path)
    exfor_files = [f for f in path.iterdir() if f.is_file()]
    pprint(exfor_files)
    exfor = x4_info(exfor_files)
    print(exfor)