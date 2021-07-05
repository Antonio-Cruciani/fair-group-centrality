import src.generators.graphs.NetworkGenerator as ng

ng.generate_network(network_type='BA', n=1000, k=10, communities_structure='bfs', threshold=3)