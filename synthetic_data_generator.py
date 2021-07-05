# This module is used to generate the Synthetic datasets with the desired properties
import src.generators.graphs.NetworkGenerator as ng

# Generating Barabasi-Albert Graphs....................................................................................
ng.generate_network(network_type='BA', n=1000, k=10, communities_structure='bfs', threshold=3)

ng.generate_network(network_type='BA', n=10000, k=15, communities_structure='bfs', threshold=3)

ng.generate_network(network_type='BA', n=1000, k=10, communities_structure='auto')


# Generating Erdos-Renyi Graphs........................................................................................
ng.generate_network(network_type='ER', n=1000, p=0.3, communities_structure='rd', number_of_communities=10)

# Generating graphs using SBM..........................................................................................
ng.generate_network(network_type='SBM', n=1000, p=0.5, q=0.5, communities_structure='rd', number_of_communities=10)
