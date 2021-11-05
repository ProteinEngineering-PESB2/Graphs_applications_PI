# Importing libraries
import pandas as pd
import json
import networkx as nx
import numpy as np
import sys, getopt
import textwrap
import os.path


def generate_graph(adjaceny_file, nodes_file, path):
    '''Crea una grafo a partir de una lista de adyacencia,
    considerando un limite superior para los pesos. En el 
    caso de que se usen interacciones como pesos se recomienda
    considerarlas todas, es decir, utilizar la opcion percentil
    con un porcentaje de 100.

    Parametros:
    adjaceny_file  -- String
                      Nombre del archivo que posee la lista de adjacencia.
    nodes_file     -- String
                      Nombre del archivo que posee la lista de nodos.
    path           -- String
                      Path para guardar el archivo.

    Retorna:
            None
            Genera archivo gpickle con el grafo.
    '''
    # Reading the adjacency list with pandas
    df_edges = pd.read_csv(adjaceny_file, header=0)

    # Reading the node list with pandas
    df_nodes = pd.read_csv(nodes_file, header=0)

    # Creating graph
    graph = nx.Graph()

    # Adding nodes
    for index, row in df_nodes.iterrows():
        graph.add_node(row['Node'])

    # Adding edges
    for index, row in df_edges.iterrows():
        graph.add_edge(row['Node_1'], row['Node_2'], weight=row['Weight'])

    # Saving the graph
    code = adjaceny_file[-8:-4]

    if adjaceny_file.find('euclidean') != -1:
        distance = 'euclidean_'
    
    elif adjaceny_file.find('cosine') != -1:
        distance = 'cosine_'
    
    else:
        distance = 'correlation_'

    if adjaceny_file.find('residues') != -1:
        file_name = path + 'graph_residues_' + distance + code
    
    elif adjaceny_file.find('interactions') != -1:
        file_name = path + 'graph_interactions_' + code
    
    else:
        file_name = path + 'graph_atoms_' + distance + code

    nx.write_gpickle(graph + '.gpickle', file_name)

    # Create json that save statistics
    Info = {'File_name': file_name,
            'Nodes': graph.number_of_nodes,
            'Edges': graph.number_of_edges}

    # Saving json
    with open(file_name + '.json', 'w') as fp:
        json.dump(Info, fp)


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
        opts, args = getopt.getopt(argv,"hp:",["help","path="])
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
    main(sys.argv[3:])
    generate_graph(sys.argv[1], sys.argv[2], Params['PATH'])

sys.exit()
