import src.generators.graphs.NetworkGenerator as ng

ng.generate_network(network_type='BA', n=1000, k=10, communities_structure='bfs', threshold=3)

#ng.generate_network(network_type='ER', n=1000, p=0.5, communities_structure='bfs', threshold=3)