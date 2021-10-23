import json
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import tqdm
import time
import os
import argparse
import sh
import requests
import multiprocessing
import numpy as np
import pandas as pd
from Bio.PDB.PDBParser import PDBParser
import sys
import urllib.request      

#get results from whatif using pdb input got
def scrapping(pdb_file, input_folder):

    op = webdriver.ChromeOptions()
    op.add_argument('headless')#Para no ver la ventana del navegador (recomendado)
    
    #create browser driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
    if pdb_file != '':
        try:
            response = "Traceback"            
            while("Traceback" in response):#Esto es para evitar errores (de whatif)
                driver.get("https://swift.cmbi.umcn.nl/servers/html/hnet.html")
                form = driver.find_elements_by_tag_name("input")[2]
                form.send_keys(os.getcwd()+"/"+input_folder+ pdb_file)
                driver.find_elements_by_tag_name("input")[3].click()
                response = "Processing .."
                while(response == "Processing .."):
                    response = driver.find_element_by_tag_name("body").text
                    time.sleep(0.5)
            route = "{}/{}{}".format(os.getcwd(), input_folder, pdb_file.replace(".pdb", ".txt"))
            f = open(route, "w")
            f.write(response)
            f.close()
        except:
            pass
    driver.close()

#check number of chain 
def check_number_chains(input_folder, pdb_file):

    parser = PDBParser()#creamos un parse de pdb
    pdb_code = pdb_file.split(".")[0]
    structure = parser.get_structure(pdb_code, input_folder+pdb_file)

    chains = 0
    for model in structure:
        for chain in model:
            chains+=1

    if chains>=2:
        return True
    else:
        return False

#check file output
def check_whatif_result(input_folder):

    list_files = os.listdir(input_folder)

    file_exist = False

    for file in list_files:
        if ".txt" in file:
            file_exist = True
            break

    return file_exist

def get_edges_from_line(line_hbond_file):

    data_validation = line_hbond_file.split(" ")
    data_validation = [value for value in data_validation if str(value) != "nan" and value!= "" and value != ")" and value != "("]

    response = []

    if "you" not in line_hbond_file:
        try:
            if len(data_validation) == 15:
                node1 = "{}-{}-{}".format(data_validation[3][1].replace("(", ""), data_validation[1].replace("(", ""), data_validation[2].replace("(", ""))
                node2 = "{}-{}-{}".format(data_validation[9][1].replace("(", ""), data_validation[7].replace("(", ""), data_validation[8].replace("(", ""))
                value_interaction = data_validation[-1]

                response = [node1, node2, value_interaction]

        except:
            pass

        try:
            if len(data_validation) == 16:
                
                node1 = "{}-{}-{}".format(data_validation[3][1].replace("(", ""), data_validation[1].replace("(", ""), data_validation[2].replace("(", ""))
                node2 = "{}-{}-{}".format(data_validation[9][1].replace("(", ""), data_validation[7].replace("(", ""), data_validation[8].replace("(", ""))
                value_interaction = data_validation[-2]

                response = [node1, node2, value_interaction]
        except:
            pass

        try:
            if len(data_validation) == 17:

                res_1 = data_validation[1]
                res_2 = data_validation[6]
                pos_chain1 = data_validation[2].split(")")
                pos_chain2 = data_validation[7].split(")")
                value_interaction = data_validation[12]

                node1= "{}-{}-{}".format(pos_chain1[1].replace("(", ""), res_1.replace("(", ""), pos_chain1[0].replace("(", ""))
                node2= "{}-{}-{}".format(pos_chain2[1].replace("(", ""), res_2.replace("(", ""), pos_chain2[0].replace("(", ""))

                response = [node1, node2, value_interaction]

        except:
            pass

        try:
            if len(data_validation) == 18:
                
                #process node 1
                res1 = data_validation[1]
                pos1 = ""
                chain1 = ""

                res2 = ""
                pos2 = ""
                chain2 = ""

                if len(data_validation[2].split(")"))>1:
                    pos1 = data_validation[2].split(")")[0]
                    chain1 = data_validation[2].split(")")[1]
                    res2 = data_validation[6]

                    pos2 = data_validation[7]
                    chain2 = data_validation[8][1]

                else:
                    pos1 = data_validation[2]
                    chain1 = data_validation[3][1]
                    res2 = data_validation[7]
                    pos2 = data_validation[8].split(")")[0]
                    chain2 = data_validation[8].split(")")[1]

                node1 = "{}-{}-{}".format(chain1.replace("(", ""), res1.replace("(", ""), pos1.replace("(", ""))
                node2 = "{}-{}-{}".format(chain2.replace("(", ""), res2.replace("(", ""), pos2.replace("(", ""))

                value_interaction = data_validation[13]

                response = [node1, node2, value_interaction]
        
        except:
            pass

        try:
            if len(data_validation) == 19:

                node1 = "{}-{}-{}".format(data_validation[3][1].replace("(", ""), data_validation[1].replace("(", ""), data_validation[2].replace("(", ""))
                node2 = "{}-{}-{}".format(data_validation[9][1].replace("(", ""), data_validation[7].replace("(", ""), data_validation[8].replace("(", ""))
                value_interaction = data_validation[14]

                response = [node1, node2, value_interaction]

        except:
            pass

        try:
            if len(data_validation) == 20:
                node1 = "{}-{}-{}".format(data_validation[3][1].replace("(", ""), data_validation[1].replace("(", ""), data_validation[2].replace("(", ""))
                node2 = "{}-{}-{}".format(data_validation[10][1].replace("(", ""), data_validation[8].replace("(", ""), data_validation[9].replace("(", ""))
                value_interaction = data_validation[15]

                response = [node1, node2, value_interaction]

        except:
            pass

        try:
            if len(data_validation) == 21:
                node1 = "{}-{}-{}".format(data_validation[3][1].replace("(", ""), data_validation[1].replace("(", ""), data_validation[2].replace("(", ""))
                node2 = "{}-{}-{}".format(data_validation[10][1].replace("(", ""), data_validation[8].replace("(", ""), data_validation[9].replace("(", ""))
                value_interaction = data_validation[16]

                response = [node1, node2, value_interaction]

        except:
            pass

    return response

#get positions from pdb using identified residues on interactions process
def get_positions_from_pdb(chain, id_data, pdb_code, input_folder):

    parser = PDBParser()#creamos un parse de pdb
    
    try:
        structure = parser.get_structure(pdb_code, "{}/{}.pdb".format(input_folder, pdb_code))
    except:
        structure = parser.get_structure(pdb_code.upper(), "{}}/{}.pdb".format(input_folder, pdb_code.upper()))
    
    atom_data = structure[0][chain][id_data]["CA"]
    coordenates = atom_data.get_coord()
    coordenates_str = "{}:{}:{}".format(coordenates[0], coordenates[1], coordenates[2])

    return coordenates_str

#process result whatif
def process_result_whatif(input_folder, pdb_file):

    name_file = input_folder+pdb_file.replace("pdb", "txt")
    file_open = open(name_file, 'r')

    #jump the first four lines
    line = file_open.readline()
    line = file_open.readline()
    line = file_open.readline()
    line = file_open.readline()

    array_interactions = []
    while line:
        line = line.replace("\n", "")       
        if "Flipped" in line:
            break
        else:
            response_interactions = get_edges_from_line(line)                        
            if len(response_interactions) == 3:
                node1 = response_interactions[0]    
                node2 = response_interactions[1]
                value_data = response_interactions[2]

                try:
                    node1_values = node1.split("-")
                    pdb_code = pdb_file.split(".")[0]
                    coordenates_str_node1= get_positions_from_pdb(node1_values[0], int(node1_values[2]), pdb_code, input_folder)
                    
                    node2_values = node2.split("-")
                    coordenates_str_node2= get_positions_from_pdb(node2_values[0], int(node2_values[2]), pdb_code, input_folder)

                    node1 = {"chain":node1_values[0], "residue": node1_values[1], "pos" : node1_values[2]}
                    pos_node1 = {"x": coordenates_str_node1.split(":")[0], "y":coordenates_str_node1.split(":")[1], "z": coordenates_str_node1.split(":")[2]}

                    node2 = {"chain":node2_values[0], "residue": node2_values[1], "pos" : node2_values[2]}
                    pos_node2 = {"x": coordenates_str_node2.split(":")[0], "y":coordenates_str_node2.split(":")[1], "z": coordenates_str_node2.split(":")[2]}

                    interaction_data = {"member1":{"info_residue":node1, "info_pos": pos_node1}, "member2":{"info_residue":node2, "info_pos": pos_node2}, "value_interaction": value_data}

                    array_interactions.append(interaction_data) 
                except:
                    pass

        line = file_open.readline()
    file_open.close()

    return array_interactions

#download pdb files from url
def dowload_pdb_code(pdb_code, input_folder):

    response = 0
    try:
        url_data = "http://files.rcsb.org/download/{}.pdb".format(pdb_code)
        pdb_file = "{}/{}.pdb".format(input_folder, pdb_code)
        urllib.request.urlretrieve(url_data, pdb_file)
    except:
        response = -1
        pass

    return response

def run_process_service(input_folder, pdb_data):

    dict_response = {}

    #process scraping
    scrapping(pdb_data, input_folder)

    if check_whatif_result(input_folder):
        dict_response.update({"status_whatif": "OK"})
        array_interactions = process_result_whatif(input_folder, pdb_data)

        dict_response.update({"detected_interactions":array_interactions})
            
    else:
        dict_response.update({"status_whatif": "ERR"})
    
    return dict_response

#arguments
input_folder = sys.argv[1]
pdb_option = int(sys.argv[2])#1: is a file, 2: is a PDB code
pdb_input = sys.argv[3]

#create dir
command = "mkdir -p {}{}".format(input_folder, pdb_input)
print(command)
os.system(command)

input_folder = "{}{}/".format(input_folder, pdb_input)

dict_response = {}

#check download or process from file
if pdb_option == 2:
    print("Download process")
    response_download = dowload_pdb_code(pdb_input, input_folder)

    if response_download == -1:
        dict_response.update({"status_download":"ERR"})

    else:
        print("Process interactions")
        response_interactions = run_process_service(input_folder, pdb_input+".pdb")
        dict_response.update({"response_service":response_interactions})

else:
    response_interactions = run_process_service(input_folder, pdb_input)
    dict_response.update({"response_service":response_interactions})

with open("{}{}_interactions_results.json".format(input_folder, pdb_input), 'w') as outfile:
    json.dump(dict_response, outfile)
