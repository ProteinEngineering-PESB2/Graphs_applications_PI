import json
import pandas as pd

# Load json
interaction_data = open('Proteins2tgf/2tgf_interactions_results.json')
interaction_data = json.load(interaction_data)['response_service']['detected_interactions']

# Create dataframe
df = pd.DataFrame(columns=['Node_1', 'Node_2', 'Weight'])

for inter in interaction_data:
    res_1 = inter['member1']['info_residue']['residue'] + (
            inter['member1']['info_residue']['pos']) + '_' + (
            inter['member1']['info_residue']['chain'])
    res_2 = inter['member2']['info_residue']['residue'] + (
            inter['member2']['info_residue']['pos']) + '_' + (
            inter['member2']['info_residue']['chain'])
    weight = inter['value_interaction']
    row = {'Node_1': res_1, 'Node_2': res_2, 'Weight': weight}
    df = df.append(row, ignore_index=True)

Name =  'Adjacency_lists/adjacency_list_interactions_2tgf'
df.to_csv(Name+'.csv', index=False)