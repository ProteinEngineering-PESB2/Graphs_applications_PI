import igraph as ig
import networkx as nx
import pandas as pd
import time
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
    try: 
        if algorithm == 'louvain':
            print('Algoritmo: Louvain')
            inicial = time.time()
            G_sub = graph.community_multilevel()
            final = time.time() - inicial
            print('Tiempo de ejecucion: {}'.format(final))
        
        elif algorithm == 'optimal_modularity':
            print('Algoritmo: Optimal modularity')
            inicial = time.time()
            G_sub = graph.community_optimal_modularity()
            final = time.time() - inicial
            print('Tiempo de ejecucion: {}'.format(final))

        elif algorithm == 'leading_eigenvector':
            print('Algoritmo: Leading eigenvector')
            inicial = time.time()
            G_sub = graph.community_leading_eigenvector()
            final = time.time() - inicial
            print('Tiempo de ejecucion: {}'.format(final))

        elif algorithm == 'spinglass':
            print('Algoritmo: Spinglass')
            inicial = time.time()
            G_sub = graph.community_spinglass()
            final = time.time() - inicial
            print('Tiempo de ejecucion: {}'.format(final))

        elif algorithm == 'label_propagation':
            print('Algoritmo: Label propagation')
            inicial = time.time()
            G_sub = graph.community_label_propagation()
            final = time.time() - inicial
            print('Tiempo de ejecucion: {}'.format(final))
            
        elif algorithm == 'infomap':
            print('Algoritmo: Infomap')
            inicial = time.time()
            G_sub = graph.community_infomap()
            final = time.time() - inicial
            print('Tiempo de ejecucion: {}'.format(final))
        
        elif algorithm == 'edge_betweenness':
            print('Algoritmo: Edge betweenness')
            inicial = time.time()
            G_sub = graph.community_edge_betweenness()
            final = time.time() - inicial
            print('Tiempo de ejecucion: {}'.format(final))

        elif algorithm == 'fast_greedy':
            print('Algoritmo: Fast greddy')
            inicial = time.time()
            G_sub = graph.community_fastgreedy()
            final = time.time() - inicial
            print('Tiempo de ejecucion: {}'.format(final))

        elif algorithm == 'walktrap':
            print('Algoritmo: Walktrap')
            inicial = time.time()
            G_sub = graph.community_walktrap()
            final = time.time() - inicial
            print('Tiempo de ejecucion: {}'.format(final))

        # Transform VertexDendrogram in VertexClustering
        if type(G_sub) == ig.clustering.VertexDendrogram:
            G_sub = G_sub.as_clustering()
    
        return G_sub
    
    except:
        return '-'


def detect_communities(graph, algorithm, code, path):
    '''
    Docstring
    '''
    # Create dataframe
    df = pd.DataFrame(columns=['Node', 'Community'])

    # Detect communities
    G_sub = select_algorithm(graph, algorithm)

    # Save communities in Dataframe
    try:
        Modularity = G_sub.modularity
        Communities = len(G_sub)
        for i in range(len(G_sub)):
            for node in G_sub[i]:
                row = {'Node': graph.vs[node]['_nx_name'], 'Community': i}
                df = df.append(row, ignore_index=True)
    except:
        Modularity = '-'
        Communities = '-'


    # Returning statistics
    return (Modularity, Communities, df)


def generate_comparison(File, algorithm_list, path):
    '''
    Docstring
    '''
    # Read the graph
    graph_nx = nx.read_gpickle(File)

    # Transform from networkx to igraph
    graph = ig.Graph.from_networkx(graph_nx)

    # Obtain the code
    code = File[-12:-8]

    # Create dataframe
    df_resumen = pd.DataFrame([code], columns=['Protein'])
    df_data = pd.DataFrame()

    print('Iniciando deteccion de comunidades')

    # Iterate in the algorithms
    for alg in algorithm_list:
        result = detect_communities(graph, alg, code, path)
        data = [[result[0], result[1]]]
        df_alg = pd.DataFrame(data, columns=['Modularity', 'Communities']) 
        df_resumen = pd.concat([df_resumen, df_alg], axis=1)

        algorithm_name = pd.DataFrame([alg], columns=['Algorithm']) 
        df_data = pd.concat([df_data, algorithm_name, result[2]], axis=1)

    # Save dataframe
    if File.find('euclidean') != -1:
        distance = 'euclidean_'
    
    elif File.find('cosine') != -1:
        distance = 'cosine_'
    
    else:
        distance = 'correlation_'

    if File.find('residues') != -1:
        sufijo = 'residues_' + distance
    
    elif File.find('interactions') != -1:
        sufijo = 'interactions_'
    
    else:
        sufijo = 'atoms_' + distance
    
    Name_resumen =  path + 'communities_comparison_' + sufijo + code
    Name_data = path + 'communities_' + sufijo + code
    df_resumen.to_csv(Name_resumen+'.csv', index=False)
    df_data.to_csv(Name_data+'.csv', index=False)

# Function parameters
Params = dict(PATH = '')

def printUsage():

    print('Usage: ' +sys.argv[0] + ' [OPTIONS]')
    print(textwrap.dedent("""
        -h, --help            : This text.
        -p, --path <VALUE>    : relative path where the csv will be saved. Default value '' (save in the current path).

        Ejemplo de uso:
        python Community_detection.py nombre_de_grafo -p ../ 
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
    main(sys.argv[2:])
    Allowed_algorithms = ['louvain', 'optimal_modularity', 'leading_eigenvector',
                         'spinglass', 'label_propagation', 'infomap',
                         'edge_betweenness', 'fast_greedy', 'walktrap']
    generate_comparison(sys.argv[1], Allowed_algorithms, Params['PATH'])

sys.exit()