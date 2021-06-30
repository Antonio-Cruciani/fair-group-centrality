import random as rnd
import networkit as nk


class community():

    def __init__(self,G,structure, size):

        self.G = G
        self.structure = structure
        self.size = size
        self.number = len(size)
        self.nodes = [v for v in self.G.iterNodes()]
        self.communities = []
        self.detectedCommunities = []





    def run(self):
        if(self.structure in ['random','Random','RANDOM']):
            self.computeRandomCommunities()
        elif(self.structure in ['BFS','bfs']):
            self.computeBFSCommunities()

    def communityDetection(self, algorithm="standard"):
        if (algorithm in ['standard', 'Standard', 'STANDARD']):
            communities = nk.community.detectCommunities(self.G)
        elif (algorithm in ['PLM', 'plm']):
            communities = nk.community.detectCommunities(self.G, algo=nk.community.PLM(self.G, True))
        elif (algorithm in ['PLP', 'plp']):
            communities = nk.community.detectCommunities(self.G, algo=nk.community.PLP(self.G))
        for setIndex in communities.getSubsetIds():
            self.detectedCommunities.append(list(communities.getMembers(setIndex)))

    def computeBFSCommunities(self):
        nodes = self.nodes
        seeds = rnd.sample(nodes,self.number)
        graph = self.G
        j = 0
        for seed in seeds:
            bfs = nk.distance.BFS(graph, seed, storePaths=True, storeNodesSortedByDistance=True).run()
            sorted_by_distance = bfs.getNodesSortedByDistance()
            self.communities.append(sorted_by_distance[0:self.size[j]])
            new_nodes = set(nodes) - set(sorted_by_distance[0:self.size[j]])
            nodes = list(new_nodes)
            graph = nk.graphtools.subgraphFromNodes(self.G, nodes)
            j+=1
        # If the method did not assign all the nodes to a community, assign the remaining at random to the communities that have
        # size less than the desidered target size.
        if(len(nodes) != 0):
            j = 0
            for elem in self.communities:
                if(len(elem) != self.size[j]):
                    target_size = self.size[j] - len(elem)
                    new_nodes = rnd.sample(nodes,target_size)
                    self.communities[j].extend(new_nodes)
                    updates = set(nodes)-set(new_nodes)
                    nodes = list(updates)
                j+=1


    def computeRandomCommunities(self):
        nodes = self.nodes
        j = 0
        for k in range(0,self.number):
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
    def get_detectedCommunities(self):
        return self.detectedCommunities