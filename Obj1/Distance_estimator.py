# Importing libraries
from Bio.PDB import PDBParser
import numpy as np
import pandas as pd
import json
import sys, getopt
import textwrap
import os.path

def estimate_euclidean_distance(atom_1, atom_2):
    '''Estima la distancia euclidena entre dos atomos de un
    modelo pdb.

    Parametros:
    atom_1 -- Atomo de pdb (Object)
              Primer atomo.
    atom_2 -- Atomo de pdb (Object) 
              Segundo atomo.

    Retorna:
            Float
            Distancia euclideana entre ambos atomos.
    '''
    distance = atom_1 - atom_2
    return distance


def estimate_cosine_similarity(atom_1, atom_2):
    '''Estima la distancia de cosenos entre dos atomos de un
    modelo pdb.

    Parametros:
    atom_1 -- Atomo de pdb (Object)
              Primer atomo.
    atom_2 -- Atomo de pdb (Object) 
              Segundo atomo.

    Retorna:
            Float
            Distancia de cosenos entre ambos atomos.
    '''
    vector_1 = atom_1.get_vector()
    vector_2 = atom_2.get_vector()
    distance = (vector_1*vector_2)/(((vector_1*vector_1)**0.5
                )*((vector_2*vector_2)**0.5))
    return distance


def estimate_manhattan_distance(atom_1, atom_2):
    '''Estima la distancia manhattan entre dos atomos de un
    modelo pdb.

    Parametros:
    atom_1 -- Atomo de pdb (Object)
              Primer atomo.
    atom_2 -- Atomo de pdb (Object) 
              Segundo atomo.

    Retorna:
            Float
            Distancia manhattan entre ambos atomos.
    '''
    vector_1 = atom_1.get_vector()
    vector_2 = atom_2.get_vector()
    distance = 0
    for i in range(3):
        distance += abs(vector_1[i]-vector_2[i])
    return distance


def name_atom(atom):
    '''Crea un string que contiene el nombre del
    atomo segun la nomenclatura adoptada en el trabajo
    (tipo de atomo_numero de residuo_cadena).

    Parametros:
    atom  -- Atomo de pdb (Object)
              Primer atomo.

    Retorna:
            String
            Nombre del atomo.
    '''
    name = atom.get_name()
    res = atom.get_parent()
    res_name = res.get_resname() + str(res.id[1])
    chain = atom.get_parent().get_parent().id
    return name+'_'+res_name+'_'+chain


def is_aminoacid(res):
    '''Revisa si el elemento en cuestion es parte
    de un aminoacido.

    Parametros:
    res  -- String
            Nombre del residuo al que pertenece el elemento
            a estudiar.

    Retorna:
            Boolean
            True si corresponde a un elemento perteneciente
            a un aminoacido, False si no.
    '''

    Allowed_aa = ['GLY', 'ALA', 'VAL', 'LEU', 'ILE', 'PHE', 'TYR', 'TRP',
                  'SER', 'THR', 'CYS', 'MET', 'PRO', 'ASP', 'GLU', 'ASN',
                  'GLN', 'LYS', 'ARG', 'HIS']
    
    return res in Allowed_aa


def create_adjacency_list(name, dist, granul, path):
    '''Crea una lista de adjacencia con los atomos como nodos 
    y las distancias como pesos.

    Parametros:
    name  -- String
             Nombre del archivo que contiene el modelo pdb de
             la proteina.
    dist  -- String
             Tipo de distancia a utilizar.
    granul  -- String
               Tipo de granularidad a utilizar.
    path  -- String
             Path para guardar el archivo.

    Retorna:
            None
            Genera archivo csv con la lista de adyacencia.
    '''
    # Reading the pdb file
    sloppyparser = PDBParser(PERMISSIVE=True)
    structure = sloppyparser.get_structure('protein', name)

    # Just analyze the first model
    model = structure[0]

    # Create dataframe
    df = pd.DataFrame(columns=['Node_1', 'Node_2', 'Weight'])

    # Residue level (Distance between alpha carbons)
    if granul == 'coarse':

        residues = list(model.get_residues())

        for i in range(len(residues)):
            for j in range(i, len(residues)):
                if i != j:
                    if (is_aminoacid(residues[i].get_resname()) and 
                        is_aminoacid(residues[j].get_resname())):
                        try:
                            atom_1 = residues[i]['CA']
                            atom_2 = residues[j]['CA']

                            if dist == 'euclidean':
                                distance = estimate_euclidean_distance(atom_1, atom_2)
                            elif dist == 'cosine':
                                distance = estimate_cosine_similarity(atom_1, atom_2)
                            elif dist == 'manhattan':
                                distance = estimate_manhattan_distance(atom_1, atom_2)
                            
                            row = {'Node_1': name_atom(atom_1), 'Node_2': name_atom(atom_2),
                                   'Weight': distance}
                            
                            df = df.append(row, ignore_index=True)

                        except:
                            atom_1 = residues[i].get_resname() + str(residues[i].id[1])
                            atom_2 = residues[j].get_resname() + str(residues[j].id[1])
                            row = {'Node_1': atom_1, 'Node_2': atom_2,
                                   'Weight': np.nan}

                            df = df.append(row, ignore_index=True)

        # Naming the file
        file_name = 'adjacency_list_distance_residues_' + name[-8:-4]
    
    # Atomic level
    if granul == 'fine':

        atoms = list(model.get_atoms())

        for i in range(len(atoms)):
            for j in range(i, len(atoms)):
                if i != j:

                    atom_1 = atoms[i]
                    atom_2 = atoms[j]

                    if (is_aminoacid(atom_1.get_parent().get_resname()) and
                        is_aminoacid(atom_2.get_parent().get_resname())):
                        try:
                            if dist == 'euclidean':
                                distance = estimate_euclidean_distance(atom_1, atom_2)
                            elif dist == 'cosine':
                                distance = estimate_cosine_similarity(atom_1, atom_2)
                            elif dist == 'manhattan':
                                distance = estimate_manhattan_distance(atom_1, atom_2)
                            
                            row = {'Node_1': name_atom(atom_1), 'Node_2': name_atom(atom_2),
                                   'Weight': distance}

                            df = df.append(row, ignore_index=True)

                        except:
                            row = {'Node_1': name_atom(atom_1), 'Node_2': name_atom(atom_2),
                                   'Weight': np.nan}

                            df = df.append(row, ignore_index=True)

        # Naming the file
        file_name = 'adjacency_list_distance_atoms_' + name[-8:-4]


    # Saving the file
    df.to_csv(path+file_name+'.csv', index=False)

    # Create json that save statistics
    Info = {'File_name': file_name,
            'Rows': df.shape[0],
            'NaN': int(df['Weight'].isnull().sum())}

    # Saving json
    with open(path+file_name+'.json', 'w') as fp:
        json.dump(Info, fp)


# Function parameters
Params = dict(DISTANCE = 'euclidean',
              GRANULARITY = 'coarse',
              PATH = '')

# Allowed values
Allowed_distances = ['euclidean', 'cosine', 'manhattan']
Allowed_granularity = ['coarse', 'fine']


def printUsage():

    print('Usage: ' +sys.argv[0] + ' [OPTIONS]')
    print(textwrap.dedent("""
        -h, --help            : This text.
        -d, --dist <VALUE>    : Distance type. Allowed values 'euclidean', 'cosine', 'manhattan'. Default value 'euclidean' .
        -g, --granul <VALUE>  : Model granularity. Allowed values 'coarse', 'fine'. Default value 'coarse' .
        -p, --path <VALUE>    : relative path where the csv will be saved. Default value '' (save in the current path) .

        Ejemplo de uso:
        python Distance_estimator.py nombre_de_archivo_pdb -d cosine -p ../ 
        """))


def main(argv):

    try:
        opts, args = getopt.getopt(argv,"hd:g:p:",["help","dist=","granul=","path="])
        for opt, arg in opts:

            if opt in ("-h", "--help"):
                printUsage()
                sys.exit()

            elif opt in ("-d", "--dist"):
                if arg in Allowed_distances:
                    Params['DISTANCE'] = arg
                else:
                    print('Distance type not allowed')
                    printUsage()
                    sys.exit(1)

            elif opt in ("-g", "--granul"):
                if arg in Allowed_granularity:
                    Params['GRANULARITY'] = arg
                else:
                    print('Granularity type not allowed')
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
    create_adjacency_list(sys.argv[1], Params['DISTANCE'],
                          Params['GRANULARITY'], Params['PATH'])


sys.exit()
