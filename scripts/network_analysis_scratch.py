import networkx as nx
import csv
%matplotlib inline
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (30.0, 20.0)

nodes = senators.copy() #make the nodes

#make the edges
from itertools import combinations
pair_list = [list(x) for x in combinations(senators, 2)]
edges = []
for edge in pair_list:
    edges.append((edge[0], edge[1]))

#graph
senate = nx.Graph()
senate.add_nodes_from(nodes)
senate.add_edges_from(edges)


print (nx.info(senate))

nx.draw(senate)

print (nx.is_connected(senate))

print (nx.number_connected_components(senate))

#look at senators of interest
senators_of_interest = [senators[0], senators[1], senators[44]]
senator_int_nodes = {}
for node in senate.nodes_iter(data=True):
    if node[0] in senators_of_interest:
        print (node)
        senator_int_nodes[node[0]] = node[0]



pos = nx.spring_layout(senate)
for key, value in outcome_information.items():
    nx.draw_networkx_nodes(senate, pos, 
                          nodelist = nodes,
                           node_size = 1000*-np.log(value),
                           #node_color = attribute['color'],
                           alpha = 0.75,
                           linewidth = 0
                          )
    nx.draw_networkx_labels(senate, pos, 
                            labels = {name : name for name, node in outcome_information.items()},
                            font_size = 14,
                            alpha = 0.5
                           )

# need to compute pairwise mutual information for edge weights
pairwise_mutual_information = []
for pair in pair_list:
    mi = calc_MI(votes[pair[0]].values, votes[pair[1]].values, 10)
    pairwise_mutual_information.append(mi)
    
#weighted edges
edges_weighted = []
for i, edge in enumerate(edges):
    edges_weighted.append((edge[0], edge[1], (pairwise_mutual_information[i])/.03))
    

#make graph with weighted edges
senate_w = nx.Graph()
senate_w.add_nodes_from(nodes)
senate_w.add_weighted_edges_from(edges_weighted)

edge_width = []
for u, v, d in senate_w.edges(data=True):
    edge_width.append(d['weight'])

    