# Importing libraries
import pandas as pd
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
        upper = np.mean(data) + np.std(data)

    elif option == 'percentile':
        upper = np.percentile(data, percent)
    
    return upper


def filter_distance(File:str, option:str, percent:int, path:str) -> None:
    """[summary]

    Args:
        File (str): [description]
        option (str): [description]
        percent (int): [description]
        path (str): [description]
    """
    # Reading the adjacency list with pandas
    df_edges = pd.read_csv(File, header=0)
    df_edges = df_edges[df_edges['Node_1'] != df_edges['Node_2']]
    df_edges.dropna(inplace=True)

    # Obtaining the code
    code = File[-8:-4]

    # Types of distance
    distance_types = ['euclidean', 'correlation', 'cosine']

    for col in distance_types:
        # Calculating the upper threshold
        upper = calculate_upper(df_edges[col], option, percent)
        
        # Filtering the values
        df_result = df_edges[['Node_1', 'Node_2', col]]
        df_result = df_result[df_result[col] <= upper]
        df_result = df_result.rename(columns={col: 'Weight'})

        # Saving the file
        if File.find('residues') != -1:
            File_name= path + 'adjacency_list_residues_' + col + '_' + code + '.csv'
        else:
            File_name= path + 'adjacency_list_atoms_' + col + '_' + code + '.csv'
        
        df_result.to_csv(File_name, index=False)


# Function parameters
Params = dict(OPTION = 'percentile',
              NUMBER = 25,
              PATH = '')

# Allowed values
Allowed_options = ['mean', 'percentile', None]


def printUsage():

    print('Usage: ' +sys.argv[0] + ' [OPTIONS]')
    print(textwrap.dedent("""
        -h, --help            : This text.
        -o, --option <VALUE>  : Method to calculate the upper threshold. Allowed values 'mean', 'percentile'. 
                                Default value percentile.
        -n, --number <VALUE>  : Number of percentile. Allowed values go from 0 to 100. Default value 25.
        -p, --path <VALUE>    : relative path where the csv will be saved. Default value '' (save in the current path).

        Ejemplo de uso:
        python Distance_filter.py nombre_de_archivo -n 10
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
    filter_distance(sys.argv[1], Params['OPTION'], Params['NUMBER'],
                   Params['PATH'])

sys.exit()
