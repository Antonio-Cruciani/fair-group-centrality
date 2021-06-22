import itertools
import networkit as nk

class GroupHarmonicCentrality:

    def __init__(self,G,k):
        self.G = G
        self.k = k

        self.nodes = [u for u in self.G.iterNodes()]

        self.groups = None
        self.groups_centralities = None



        self.max_group = None
        self.GHC_max_group = None




    def findsubsets(self,s, k):
        return list(itertools.combinations(s, k))

    def HarmonicOfGroup(self,group):
        distances = []
        nk.traversal.Traversal.BFSfrom(self.G, group, lambda u, dist: distances.append(1./dist))

        return sum(distances)


    def compute_groups_centralities(self):
        self.groups = self.findsubsets(self.nodes,self.k)
        self.groups_centralities = []
        for group in self.groups:
            self.groups_centralities.append(self.HarmonicOfGroup(group))

        # getting the group of k nodes that maximizes the Group Harmonic Centrality
        index = 0
        j = 0
        maximum = 0

        for elem in self.groups_centralities:
            if(elem>maximum):
                maximum = elem
                index = j
            j+=1

        self.max_group = self.groups[index]
        self.GHC_max_group = self.groups_centralities[index]


