import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import exfor_parser

# 1. Parse the EXFOR data
file_path = ["Yb.txt",  "HO-165(G,N)67-HO-164.txt", "Gd160(g,n).txt","La(g,n).txt", "Ce(g,n).txt","Eu(g,n).txt","Tb(g,n).txt"]
E, cs, targets, products, projectiles, ejectiles = exfor_parser.parse_x4(file_path)

data_dict = {
    "Energy_MeV": np.concatenate(E), 
    "Cross_Section_mb": np.concatenate(cs),
    "Target": np.concatenate(targets),
    "Projectile": np.concatenate(projectiles),
    "Ejectile": np.concatenate(ejectiles),
    "Product": np.concatenate(products)
}

df = pd.DataFrame(data_dict)
df["Target"]= pd.to_numeric(df["Target"])
print(f"Targets : {df['Target'].unique()}")

nuclear_moments = pd.read_csv("nuclear_moments.csv")

#merge exfor data(E, Ain,Aout,Symbol,cross section) with Q, u based on Ain as primary key
df1 = pd.merge(df, nuclear_moments, on='Target', how='left')

#filter non zero and Nan from Q , u and E>48 MeV
filter_df = df1[((df1["Q"] != 0) & df1["Q"].notna()) & ((df1["mu_N"] != 0) & df1["mu_N"].notna())]
filter_df = filter_df.drop(filter_df[filter_df['Energy_MeV'] > 48].index)
print(filter_df)

scaled_df = filter_df.copy()
scaled_df = scaled_df.drop(columns=['Projectile', 'Ejectile', 'Product', 'symbol'])

#Z Normalization (z = (x-u)/σ^2 )
#Energy normalisation : Done
#Target normalisation : All elements to be added 
scaler = StandardScaler().set_output(transform="pandas")
scaled_df = scaler.fit_transform(scaled_df)
print(scaled_df['Target'])
#scaled_df['Target'].hist(bins=50)
#plt.show()







