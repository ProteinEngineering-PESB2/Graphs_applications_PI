# Importing libraries
import json
import pandas as pd

# Load json
Data = open('Resultados.json')
Data = json.load(Data)

# Generating a dataframe
df = pd.DataFrame(columns=['Categoria', 'All alpha proteins', 'All beta proteins',
                           'Alpha and beta proteins (a+b)', 'Alpha and beta proteins (a/b)',
                           'Small proteins'])

# Dict to save data
row = {}

for categoria in Data.keys():
    row.update({'Categoria': categoria})
    total = 0

    for SCOP in Data[categoria].keys():
        contenido = len(Data[categoria][SCOP])
        row.update({SCOP: contenido})
        total += contenido

    row.update({'Total': total})
    df = df.append(row, ignore_index=True)

# Saving file
df.to_excel('Resultado_estadisticas.xlsx', index=False)


