import json
import pandas as pd
import sys, getopt
import textwrap
import os

def process_json(File, path):
        '''
        Docstring
        '''
        # Load json
        interaction_data = open(File)
        interaction_data = json.load(interaction_data)['response_service']['detected_interactions']

        # Find the code
        code = File[-30:-26]

        # Create dataframe
        df = pd.DataFrame(columns=['Node_1', 'Node_2', 'Weight'])

        for inter in interaction_data:
                res_1 = 'CA_' + inter['member1']['info_residue']['residue'] + (
                        inter['member1']['info_residue']['pos']) + '_' + (
                        inter['member1']['info_residue']['chain'])
                res_2 = 'CA_' + inter['member2']['info_residue']['residue'] + (
                        inter['member2']['info_residue']['pos']) + '_' + (
                        inter['member2']['info_residue']['chain'])
                weight = inter['value_interaction']
                row = {'Node_1': res_1, 'Node_2': res_2, 'Weight': weight}
                row_2 = {'Node_1': res_2, 'Node_2': res_1, 'Weight': weight}
                df = df.append(row, ignore_index=True)
                df = df.append(row_2, ignore_index=True)

        Name =  path + 'adjacency_list_interactions_' + code
        df.to_csv(Name + '.csv', index=False)


# Function parameters
Params = dict(PATH = '')

def printUsage():

    print('Usage: ' +sys.argv[0] + ' [OPTIONS]')
    print(textwrap.dedent("""
        -h, --help            : This text.
        -p, --path <VALUE>    : Relative path where the csv will be saved. Default value '' (save in the current path).

        Ejemplo de uso:
        python Process_json.py nombre_de_json -p ../ 
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
    process_json(sys.argv[1], Params['PATH'])

sys.exit()