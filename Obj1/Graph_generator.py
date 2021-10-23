# Importing libraries
import pandas as pd
import networkx as nx
import numpy as np
import sys, getopt
import textwrap
import os.path

def calculate_upper(data, option, percent):
    '''Calcula el limite superior para considerar las distancias.

    Parametros:
    data  -- Dataframe
             Set de datos sobre el que se calcula el parametro deseado.
    option  -- String
               Método a utilizar.
    percent  -- Int
                Porcentaje a considerar para el metodo del percentil.

    Retorna:
            Float
            Limite superior a considerar.
    '''
    if option == 'mean':
        upper = np.mean(data) - np.std(data)

    elif option == 'percentile':
        upper = np.percentile(data, percent)
    
    return upper


def generate_graph(file, option, percent, path):
    '''Crea una grafo a partir de una lista de adyacencia,
    considerando un limite superior para los pesos. En el 
    caso de que se usen interacciones como pesos se recomienda
    considerarlas todas, es decir, utilizar la opcion percentil
    con un porcentaje de 100.

    Parametros:
    file  -- String
             Nombre del archivo que la lista de adjacencia.
    option  -- String
               Metodo con el que se calculara el limite superior.
    percent  -- Int
                Porcentaje a considerar para el metodo del percentil.
    path  -- String
             Path para guardar el archivo.

    Retorna:
            None
            Genera archivo gpickle con el grafo.
    '''
    # Reading the adjacency list with pandas
    df = pd.read_csv(file, header=0)
    df.dropna(inplace=True)

    # Creating graph
    G = nx.Graph()

    # Calculating upper threshold
    upper = calculate_upper(df['Weight'], option, percent)

    # Iterating over rows
    for index, row in df.iterrows():
        Weight = row['Weight']
        if Weight <= upper:
            G.add_edge(row['Node_1'], row['Node_2'], weight=row['Weight'])
        else:
            G.add_node(row['Node_1'])
            G.add_node(row['Node_2'])
    
    # Saving the graph
    code = file[-8:-4]
    file_name = 'graph_' + code + '.gpickle'
    nx.write_gpickle(G, path + file_name)


# Function parameters
Params = dict(OPTION = 'percentile',
              NUMBER = 25,
              PATH = '')

# Allowed values
Allowed_options = ['mean', 'percentile']


def printUsage():

    print('Usage: ' +sys.argv[0] + ' [OPTIONS]')
    print(textwrap.dedent("""
        -h, --help            : This text.
        -o, --option <VALUE>  : Method to calculate the upper threshold. Allowed values 'mean', 'percentile'. 
                                Default value 'percentile'.
        -n, --number <VALUE>  : Number of percentile. Allowed values go from 0 to 100. Default value 25.
        -p, --path <VALUE>    : relative path where the csv will be saved. Default value '' (save in the current path).

        Ejemplo de uso:
        python Graph_generator.py nombre_de_archivo -n 10
        """))


def main(argv):

    try:
        opts, args = getopt.getopt(argv,"ho:n:p:",["help","option=","number=","path="])
        for opt, arg in opts:

            if opt in ("-h", "--help"):
                printUsage()
                sys.exit()

            elif opt in ("-o", "--option"):
                if arg in Allowed_options:
                    Params['OPTION'] = arg
                else:
                    print('Option not allowed')
                    printUsage()
                    sys.exit(1)

            elif opt in ("-n", "--number"):
                if int(arg) >= 0 and int(arg) <= 100:
                    Params['NUMBER'] = int(arg)
                else:
                    print('Percentil not allowed')
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
    generate_graph(sys.argv[1], Params['OPTION'], Params['NUMBER'],
                   Params['PATH'])

sys.exit()
