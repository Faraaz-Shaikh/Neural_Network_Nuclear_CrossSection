import pandas as pd
import numpy as np
from exfor_parserpy import read_exfor
from exfor_parserpy.trafos import depointerfy, uncommonfy, unitfy

#file_path = ["X4R7574_x4.txt"]

def parse_x4(file_path):

    E = []
    cs = []
    targets = []
    products = []
    projectiles = []
    ejectiles = []
    
    # Loop through all exfor files from folder
    for file in file_path:

        #read exfor file
        raw_dict = read_exfor(file)

        # FIX 1: Add reactify() to your chain of transformers!
        clean_dict = unitfy(uncommonfy(depointerfy(raw_dict)))
        #print(f"x4 dictionary \n {clean_dict}")

        # Get the Entry ID 
        entry_id = [k for k in clean_dict.keys() if not k.startswith('--')]
        print(f"entry id : {entry_id}")

        #Entry ID Loop 
        for current_entry in entry_id:

            # Find all data subentries for this specific Entry id other than '001' for bibliography and metadata keys
            subentries = [s for s in clean_dict[current_entry].keys() if not s.endswith('001') and not s.startswith('__')]

            # SubEntry Loop
            for sub_id in subentries:
                
                print(f"Reading Entry: {current_entry}, Subentry: {sub_id}")

                # Access data based on entry id and subetry
                data_dict = clean_dict[current_entry][sub_id]["DATA"]["DATA"]
                
                reaction_data = clean_dict[current_entry][sub_id]['BIB']['REACTION']
                #print(f"reaction : {reaction_data}")

                #(58-CE-142(G,N)58-CE-141,,SIG)
                
                target = reaction_data[7:10]
                product = reaction_data[21:24]
                projectile = reaction_data[11:12]
                ejectile = reaction_data[13:14]
                print(f"{target}({projectile},{ejectile}){product}")

                #print(f"data dict keys : {data_dict.keys()}")
                
                # Find Energy and cs columns
                columns = [i for i in data_dict.keys() if i.startswith('EN') or i.startswith('DATA')]

                columns = [i for i in columns if not i.endswith('ERR')]

                print(f"columns: {columns}")

                # Append and return list
                E.append(data_dict[columns[0]])
                cs.append(data_dict[columns[1]])
                
                num_data_points = len(data_dict[columns[0]])
                targets.append([target] * num_data_points)
                projectiles.append([projectile] * num_data_points)
                ejectiles.append([ejectile] * num_data_points)
                products.append([product] * num_data_points)
                print(f"reaction : {reaction_data}")

    return E, cs, targets, products, projectiles, ejectiles 

#parse_x4(file_path)
