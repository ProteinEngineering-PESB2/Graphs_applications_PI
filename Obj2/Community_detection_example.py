import igraph as ig
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import json

# Reading the graph
G = nx.read_gpickle('Graphs/graph_2tgf.gpickle')

# Transforming from networkx to igraph
G_ig = ig.Graph.from_networkx(G)

# Create dataframe
df = pd.DataFrame(columns=['Node', 'Community'])

# Multi-level (Louvain)
kc = G_ig.community_multilevel()
to_plot = []

for i in range(len(kc)):
    community = []
    for node in kc[i]:
        row = {'Node': G_ig.vs[node]['_nx_name'], 'Community': i}
        df = df.append(row, ignore_index=True)
        community.append(G_ig.vs[node]['_nx_name'])
    to_plot.append(community)

# Saving dataframe
Name = 'Test_community_Louvain.csv'
df.to_csv(Name, index=False)

# Create json that save statistics
Info = {'File_name': Name,
        'Modularity' : kc.modularity}

# Saving json
Name_json = 'Info.json'
with open(Name_json, 'w') as fp:
    json.dump(Info, fp)

# Read the graph
plt.figure(0, figsize=[18, 9])
pos = nx.spring_layout(G, seed=10)

nx.draw_networkx_nodes(G, pos, nodelist=to_plot[0], node_color= 'r', node_size=1800)
nx.draw_networkx_nodes(G, pos, nodelist=to_plot[1], node_color= 'g', node_size=1800)
nx.draw_networkx_nodes(G, pos, nodelist=to_plot[2], node_color= 'b', node_size=1800)
nx.draw_networkx_nodes(G, pos, nodelist=to_plot[3], node_color= 'y', node_size=1800)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

# Create the axis
ax = plt.gca()
ax.margins(0.08)
plt.axis("off")
plt.tight_layout()

# Show the graph
plt.show()


# Moving in the graph
# for vs in G_ig.vs:
#     print(vs['_nx_name'])

# for es in G_ig.es:
#     print(G_ig.vs[es.source]['_nx_name'])
#     print(G_ig.vs[es.target]['_nx_name'])
#     print(es['weight'])

# # Communities
# # Optimal Modularity
# kc = G_ig.community_optimal_modularity()
# print(kc.subgraphs)

# # Eigenvectors
# kc = G_ig.community_leading_eigenvector()
# print(type(kc))

# # Spinglass
# kc = G_ig.community_spinglass()
# print(type(kc))

# # Label propagation
# kc = G_ig.community_label_propagation()
# print(type(kc))

# # Multi-level
# kc = G_ig.community_multilevel()
# print(type(kc))

# # Info Map
# kc = G_ig.community_infomap()
# print(type(kc))

# # Edge Betweenness
# kc = G_ig.community_edge_betweenness()
# print(kc.optimal_count)

# # FastGreedy
# kc = G_ig.community_fastgreedy()
# print(kc.optimal_count)

# # Walktrap
# kc = G_ig.community_walktrap()
# print(kc.optimal_count)
