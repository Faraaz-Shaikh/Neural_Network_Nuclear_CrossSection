from pathlib import Path
from pprint import pprint
import pandas as pd
import numpy as np
from talys_class import Talys

t = Talys()

targets = [["Zr", 90, 40]]
proj = "g"
ejec =  "n"
for target in targets:
    exfortables_path = t.exfortables_dir / f"{proj}/{target[0]}-{target[1]}/{proj}-{ejec}/xs"
    print(exfortables_path)
    residualA = target[1] - 1
    output_dir = t.output_dir / f"{target[0]}-{target[1]}"
    #print(f"{target[0]}, path: {output_dir}")
    talys_files = [f for f in output_dir.iterdir() if f.is_file() and f.name.startswith(f"rp{str(target[2]).zfill(3)}{str(str(residualA).zfill(3))}")]
    #pprint(talys_files)
    energy = np.array([])
    talys_dict = {}
    for f in talys_files:
        ldmodel = f.name[-7:-4]
        print(f"ld: {ldmodel}, {f.name}")
        df1 = pd.read_csv(f, names=["Energy(MeV)", "Cross_Section"])
        energy = df1["Energy(MeV)"]
        cs = df1["Cross_Section"].to_numpy()
        talys_dict[f"Cross_Section{ldmodel}(mb)"] = cs

    talys_dict["Energy(MeV)"] = energy
    talys_dict = dict(reversed(talys_dict.items()))
    talys_df = pd.DataFrame(talys_dict)
    talys_df = talys_df.drop(0)
    print(f"talys \n {talys_df}")

    exfor_files = [f for f in exfortables_path.iterdir() if f.is_file()]
    pprint(exfor_files)
    exfor_df = t.x4_info(exfor_files)
    # exfor_df["Cross_Section(Barns)"] = exfor_df["Cross_Section(Barns)"]*1000
    exfor_df["Cross_Section(Barns)"] *= 1000
    exfor_df["dcs"] *= 1000
    exfor_df = exfor_df.rename(columns={"Cross_Section(Barns)": "Cross_Section(mb)"})
    exfor_df.sort_values(by="year")
    exfor_df = exfor_df.drop_duplicates(keep="first")
    
    print(f"exfor \n {exfor_df}")


    # Standardize Energy formatting to 2 decimal places in both DataFrames
    talys_df["Energy(MeV)"] = talys_df["Energy(MeV)"].astype(float).round(2)
    talys_df["Cross_Sectionld1(mb)"] = talys_df["Cross_Sectionld1(mb)"].astype(float).round(2)
    talys_df["Cross_Sectionld2(mb)"] = talys_df["Cross_Sectionld2(mb)"].astype(float).round(2)
    talys_df["Cross_Sectionld3(mb)"] = talys_df["Cross_Sectionld3(mb)"].astype(float).round(2)

    exfor_df["Energy(MeV)"] = exfor_df["Energy(MeV)"].astype(float).round(2)
    exfor_df["Cross_Section(mb)"] = exfor_df["Cross_Section(mb)"].astype(float).round(2)
    exfor_df["dcs"] = exfor_df["dcs"].astype(float).round(4)


    # Perform the right merge to keep all EXFOR points aligned with available TALYS rows
    df_merged = pd.merge(talys_df, exfor_df, on="Energy(MeV)", how="right")
    df_merged = df_merged.dropna(axis=0)
    df_merged["chi2_ld1"] = ((df_merged["Cross_Sectionld1(mb)"] - df_merged["Cross_Section(mb)"])/df_merged["dcs"])**2
    df_merged["chi2_ld2"] = ((df_merged["Cross_Sectionld2(mb)"] - df_merged["Cross_Section(mb)"])/df_merged["dcs"])**2
    df_merged["chi2_ld3"] = ((df_merged["Cross_Sectionld3(mb)"] - df_merged["Cross_Section(mb)"])/df_merged["dcs"])**2
    # df_merged = pd.merge(talys_df, exfor_df, on='Energy(MeV)', how='inner')
    print(df_merged)







    




