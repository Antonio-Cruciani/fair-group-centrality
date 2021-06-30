import random as rnd
import networkit as nk


class community():

    def __init__(self,G,structure, size):

        self.G = G
        self.structure = structure
        self.size = size
        self.number = len(size)
        self.nodes = [v for v in self.G.iterNodes()]
        self.communities = None




    def run(self):
        if(self.structure in ['random','Random','RANDOM']):
            self.computeRandomCommunities()
        elif(self.structure in ['BFS','bfs']):
            self.computeBFSCommunities()


    def computeBFSCommunities(self):
        nodes = self.nodes
        seeds = rnd.sample(nodes,self.size)
        graph = self.G
        j = 0
        for seed in seeds:
            bfs = nk.distance.BFS(graph, seed, storePaths=True, storeNodesSortedByDistance=True).run()
            sorted_by_distance = bfs.getNodesSortedByDistance()
            self.communities.append(sorted_by_distance[0:self.structure[j]])
            new_nodes = set(nodes) - set(sorted_by_distance[0:self.structure[j]])
            nodes = list(new_nodes)
            graph = nk.graphtools.subgraphFromNodes(self.G, nodes)
            j+=1


    def computeRandomCommunities(self):
        nodes = self.nodes
        j = 0
        for k in range(0,self.communitiesNumber):
            self.communities.append(rnd.sample(nodes, self.size[j]))
            new_nodes = set(nodes) - set(self.communities[j])
            nodes = list(new_nodes)
            j+=1

    def get_communities(self):
        return self.communities
    def get_G(self):
        return self.G
    def get_size(self):
        return self.size
    def get_structure(self):
        return self.structure