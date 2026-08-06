import pandas as pd
file = input('csv file to read: ')
df = pd.read_csv(file)
print(df.columns.tolist())
df1 = df[(df['symbol'] == 'Sn')]
print(df1[['a', 'symbol', 'energy [keV]', 'magnetic dipole [nm]', 'electric quadrupole [b]']])

