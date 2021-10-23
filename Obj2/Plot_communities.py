import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

def generate_colors(n, seed=10):
    '''Genera una secuencia de n disitintas tuplas de 3 numeros
    que identifican un color en la escala RGB.

    Parametros:
    n  -- Int
          Numero de colores a generar.
    seed (optional) -- Int
                       Semilla para fijar la pseudo aleatoriedad
                       del metodo.

    Retorna:
            Lista
            Contiene las tuplas con los colores.
    '''
    # Get the seed
    np.random.seed(seed)

    # Create list
    colors = []

    # Save differents colors
    for i in range(n):
        row = tuple(np.random.uniform(size=3))

        while row in colors:
            row = tuple(np.random.uniform(size=3))

        colors.append(row)
    
    return colors


def plot_communities(graph, communities):
    '''Crea una representacion grafica del grafo y las comunidades
    de este.

    Parametros:
    graph  -- String
             Nombre del archivo gpickle del grafo
    communities  -- String
                    Nombre del archivo que contiene la particion
                    en comunidades del grafo.

    Retorna:
            None
            Genera una imagen que representa el grafo y su particion.
    '''
    # Reading the list of communities
    df = pd.read_csv(communities)

    # Obtain the number of communities
    N = max(df['Community']) + 1

    # Read the graph
    G = nx.read_gpickle(graph)

    # Create figure
    plt.figure(0, figsize=[18, 9])
    pos = nx.spring_layout(G, seed=10)

    # Creating color palette
    color = generate_colors(N, seed=10)

    # Ploting the nodes
    for i in range(N):
        node_list = list(df[df['Community'] == i]['Node'])
        color_node = np.array([color[i], ])
        nx.draw_networkx_nodes(G, pos, nodelist=node_list, node_color= color_node, node_size=1800)

    # Ploting the edges
    nx.draw_networkx_edges(G, pos)

    # Ploting the labels
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

    # Create the axis
    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()

    # Show the plot
    plt.show()

if __name__ == "__main__":
    plot_communities(sys.argv[1], sys.argv[2])

sys.exit()

#plot_communities('Graphs/graph_2tgf.gpickle', 'communities_2tgf.csv')