# Importing libraries
import pandas as pd
import numpy as np
import sys, getopt
import textwrap
import os.path

def generate_node_list(File:str, path:str):
    """[summary]

    Args:
        File (str): [description]
        path (str): [description]
    """
    # Reading the adjacency list with pandas
    df = pd.read_csv(File, header=0)

    # Obtaining nodes
    nodes = df['Node_1'].unique()

    # Generating data frame
    df_node = pd.DataFrame(nodes, columns=['Node'])

    code = File[-8:-4]
    
    # Saving the file
    if File.find('residues') != -1:
        File_name= path + 'node_list_residues_' + code + '.csv'
    else:
        File_name= path + 'node_list_atoms_' + code + '.csv'

    df_node.to_csv(File_name, index=False)


# Function parameters
Params = dict(PATH = '')


def printUsage():

    print('Usage: ' +sys.argv[0] + ' [OPTIONS]')
    print(textwrap.dedent("""
        -h, --help            : This text.
        -p, --path <VALUE>    : relative path where the csv will be saved. Default value '' (save in the current path).

        Ejemplo de uso:
        python Graph_generator.py nombre_de_lista_de_adyacencia nombre_de_lista_de_nodos -p ../
        """))


def main(argv):

    try:
        opts, args = getopt.getopt(argv,"hp:",["help", "path="])
        for opt, arg in opts:

            if opt in ("-h", "--help"):
                printUsage()
                sys.exit()

            elif opt in ("-p", "--path"):
                if os.path.exists(arg):
                    Params['PATH'] = arg
                else:
                    print('Path invalido')
                    printUsage()
                    sys.exit(1)

    except getopt.GetoptError as e:
        sys.stderr.write("ERROR: %s\n\n\n" % e.msg)
        printUsage()
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[2:])
    generate_node_list(sys.argv[1], Params['PATH'])

sys.exit()
