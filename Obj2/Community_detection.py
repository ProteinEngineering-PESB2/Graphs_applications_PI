import igraph as ig
import networkx as nx
import pandas as pd
import sys, getopt
import textwrap
import os.path
import json

def select_algorithm(graph, algorithm):
    '''Utiliza el algoritmo indicado para detectar
    comunidades en un grafo.

    Parametros:
    graph -- graph (Object)
             Grafo a estudiar.
    algorithm --  String
                  Nombre del método a usar
    Retorna:
            VertexDendrogram or VertexClustering (Object)
            Objeto con la particion realizada.
    '''
    # Detecting communities
    if algorithm == 'louvain':
        G_sub = graph.community_multilevel()
    
    elif algorithm == 'optimal_modularity':
        G_sub = graph.community_optimal_modularity()

    elif algorithm == 'leading_eigenvector':
        G_sub = graph.community_leading_eigenvector()

    elif algorithm == 'spinglass':
        G_sub = graph.community_spinglass()

    elif algorithm == 'label_propagation':
        G_sub = graph.community_label_propagation()

    elif algorithm == 'infomap':
        G_sub = graph.community_infomap()
    
    elif algorithm == 'edge_betweenness':
        G_sub = graph.community_edge_betweenness()

    elif algorithm == 'fast_greedy':
        G_sub = graph.community_fastgreedy()

    elif algorithm == 'walktrap':
        G_sub = graph.community_walktrap()
    
    return G_sub


def detect_communities(File, algorithm, path):
    '''Detecta comunidades en un grafo y genera un
    archivo csv que guarda la particion calculada.

    Parametros:
    File  -- String
             Nombre del archivo que contiene el grafo a estudiar.
    algorithm --  String
                  Nombre del método a usar para detectar
                  comunidades.
    path  -- String
             Path para guardar el archivo.

    Retorna:
            None
            Genera archivo csv en que se indica a la comunidad
            que pertenece cada nodo.
    '''
    # Read the graph
    G_nx = nx.read_gpickle(File)

    # Transform from networkx to igraph
    G = ig.Graph.from_networkx(G_nx)

    # Create dataframe
    df = pd.DataFrame(columns=['Node', 'Community'])

    # Detect communities
    G_sub = select_algorithm(G, algorithm)

    # Transform VertexDendrogram in VertexClustering
    if type(G_sub) == ig.clustering.VertexDendrogram:
        G_sub = G_sub.as_clustering()

    # Save communities in Dataframe
    for i in range(len(G_sub)):
        for node in G_sub[i]:
            row = {'Node': G.vs[node]['_nx_name'], 'Community': i}
            df = df.append(row, ignore_index=True)

    # Save dataframe
    Name =  path + 'communities_' + File[-12:-8]
    df.to_csv(Name+'.csv', index=False)

    # Create json that save statistics
    Info = {'File_name': Name+'.csv',
            'Modularity' : G_sub.modularity,
            'Algorithm' : algorithm,
            'Communities': len(G_sub)}

    # Saving json
    with open(Name+'.json', 'w') as fp:
        json.dump(Info, fp)


# Function parameters
Params = dict(ALG = 'louvain',
              PATH = '')

# Allowed values
Allowed_options = ['louvain', 'optimal_modularity', 'leading_eigenvector',
                   'spinglass', 'label_propagation', 'infomap', 'edge_betweenness',
                   'fast_greedy', 'walktrap']


def printUsage():

    print('Usage: ' +sys.argv[0] + ' [OPTIONS]')
    print(textwrap.dedent("""
        -h, --help            : This text.
        -a, --alg <VALUE>     : Algorithm used to detect communities. Allowed values louvain', 
                               'optimal_modularity', 'leading_eigenvector', 'spinglass', 
                               'label_propagation', 'infomap', 'edge_betweenness', 'fast_greedy',
                               'walktrap'. Default value 'louvain'.
        -p, --path <VALUE>    : relative path where the csv will be saved. Default value '' (save in the current path).

        Ejemplo de uso:
        python Community_detection.py nombre_de_grafo -a spinglass -p ../ 
        """))


def main(argv):

    try:
        opts, args = getopt.getopt(argv,"ha:p:",["help","alg=","path="])
        for opt, arg in opts:

            if opt in ("-h", "--help"):
                printUsage()
                sys.exit()

            elif opt in ("-a", "--alg"):
                if arg in Allowed_options:
                    Params['ALG'] = arg
                else:
                    print('Algorithm not allowed')
                    printUsage()
                    sys.exit(1)

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
    detect_communities(sys.argv[1], Params['ALG'], Params['PATH'])

sys.exit()