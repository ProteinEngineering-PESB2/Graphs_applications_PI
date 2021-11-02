"""
Script que genera un json con las ids asociadas a todas las
categorias de proteina que cumplan con cierto parametro.
"""
# Importando las librerias
import pandas as pd
import requests
import json


def RCSB_Search(s, Query):
    '''Realiza una consulta vía API a la base de datos RCSB.

    Parametros:
    s     -- Sesion de requests
            Sesion iniciada para realizar las consultas.
    Query -- Dict
            Contiene los parámetros de la busqueda a realizar,
            según lo descrito en https://search.rcsb.org/index.html

    Retorna:
            Dict
            Contiene el resultado de la consulta realizada, según los
            parametros indicados.
    '''

    # URL de consulta
    URL = f'https://search.rcsb.org/rcsbsearch/v1/query?json={Query}'

    # Realizando consulta
    response = s.post(URL, json=Query,
                      headers={'Content-Type': 'application/json'})

    # Revisando la respuesta
    if response.status_code == 200:
        response = json.loads(response.content.decode("UTF-8"))

    return response


def Create_Dict(File, Protein_type, Structure_type, Dict):
    '''Procesa los resultados de la consulta realizada a RCSB,
    asociando una lista de ids con su categoria correspondiente,
    actualizando un diccionario con estos datos.

    Parametros:
    File -- Dict
            Contiene el resultado de la consulta realizada a la
            API de RCSB.
    Name -- String
            Corresponde al nombre de la categoria consultada.
    Dict -- Dict
            Es utilizado para guardar las ids asociadas a las
            distintas categorias, actualizandose en cada llamada.

    Retorna:
            None
    '''
    # Creando una lista para guardar las ids
    List = []

    # Extrayendo las ids asociadas con una categoria
    if type(File) is dict:
        for protein in File['result_set']:
            List.append(protein['identifier'])

    # Actualizando el diccionario
    Dict[Protein_type].update({Structure_type: List})


# Abriendo el archivo que contiene las categorias funcionales
protein_categories = pd.read_csv('Categorias.csv', header=0, dtype='str')
structural_categories = pd.read_csv('SCOP_Classification.csv', header=0, dtype='str')

# Creando la sesion
s = requests.session()

# Creando consulta
f = open("Search.json", "r")
content = f.read()
Search = json.loads(content)

# Diccionario en el que se guardaran las ids
Clasificacion = {}

# Filtrando segun las distintas clasificaciones
for index_prot, row_prot in protein_categories.iterrows():
    Search['query']['nodes'][2]['parameters']['value'] = row_prot['CATEGORIA']
    Clasificacion.update({row_prot['CATEGORIA']: {}})
    
    for index_str, row_str in structural_categories.iterrows():
        Search['query']['nodes'][6]['nodes'][0]['parameters']['value'] = row_str['SCOP']
        result = RCSB_Search(s, Search)
        Create_Dict(result, row_prot['CATEGORIA'], row_str['SCOP'], Clasificacion)

# Creando archivo .json para guardar la clasifiacion
with open('Resultados.json', 'w') as fp:
    json.dump(Clasificacion, fp)

s.close()
