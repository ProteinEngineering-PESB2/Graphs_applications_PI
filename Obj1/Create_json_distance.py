import json
import sys, getopt
import textwrap
import os

def generate_json_distance(input:str, path:str):
    """[summary]

    Args:
        input (str): [description]
        path (str): [description]
    """
    # Obtaining the code
    code = input[-8:-4]

    # Coarse granularity
    File_name = path + 'distance_residues_' + code + '.json'
    Output = path + 'distance_list_residues_' + code + '.csv'

    Info = {"pdb_input": input, "granularity": 'coarse', "name_output": Output}

    with open(File_name, 'w') as fp:
        json.dump(Info, fp)
    
    # Fine granularity
    File_name = path + 'distance_atoms_' + code + '.json'
    Output = path + 'distance_list_atoms_' + code + '.csv'
    Info['granularity'] = 'fine'
    Info['name_output'] = Output

    with open(File_name, 'w') as fp:
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
    generate_json_distance(sys.argv[1], Params['PATH'])

sys.exit()
    