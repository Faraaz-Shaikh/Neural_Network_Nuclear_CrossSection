import numpy as np  
#import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import os
import requests
from pprint import pprint

#----------------------------------------------------------------------------------------------
# Paths and url variables
exfortables_path = Path("/media/faraaz/Data_faru_lnx/College/MSc/Project/exfor/Neural_Network_Nuclear_CrossSection/exfortables")
url = "https://nds.iaea.org/dataexplorer/api/reactions/xs"
headers = {"User-Agent": "DataExplorer/1.0"}


def fetch_exfor(params):
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        id = data.get('aggregations', {})
        for id, details in id.items():
            print(f"Current ID: {id}")
            author = details.get("author", [])
            print(author)
            datatable = details.get("datatable", [])
            #pprint(datatable)
            Energy = datatable['en_inc']
            cross_section = datatable['data']
            dcs = datatable['ddata']
            dict = {" Energy": Energy, "Cross_Section": cross_section, "dcs": dcs}
            df = pd.DataFrame(dict)
            df.to_csv(exfortables_path / f"{params["target_elem"]}{params["target_mass"]}-{author}.csv")
            print(df)
        #pprint(data)
#---------------------------------------------------------------------------------------------------------
# Input list of nuclei [element, A]
nuclei = [["Gd", "160"],["Gd", "159"]]
for nuclei in nuclei:
    print(nuclei)
    element, A = nuclei[0], nuclei[1]
    params = {"target_elem": {element}, "target_mass": {A}, "reaction": "g,n", "table": "true"}
    print(f"Fetching data for {nuclei}")
    fetch_exfor(params)

