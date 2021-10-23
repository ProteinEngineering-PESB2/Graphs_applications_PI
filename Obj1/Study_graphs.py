import os
from Plot_communities import *

# Protein: 2tgf

# Graph 
# Distance
os.system('python Graph_generator.py Adjacency_lists/adjacency_list_residues_2tgf.csv -o percentile -n 25 -p Graphs/Distance/')

# Interaction
os.system('python Graph_generator.py Adjacency_lists/adjacency_list_interactions_2tgf.csv -o percentile -n 100 -p Graphs/Interactions/')


# Communities
# Distance
os.system('python Community_detection.py Graphs/Distance/graph_2tgf.gpickle -p Graphs/Distance/')

# Interaction
os.system('python Community_detection.py Graphs/Interactions/graph_2tgf.gpickle -p Graphs/Interactions/')


# Plot
# Distance
plot_communities('Graphs/Distance/graph_2tgf.gpickle', 'Graphs/Distance/communities_2tgf.csv')

# Interaction
plot_communities('Graphs/Interactions/graph_2tgf.gpickle', 'Graphs/Interactions/communities_2tgf.csv')


