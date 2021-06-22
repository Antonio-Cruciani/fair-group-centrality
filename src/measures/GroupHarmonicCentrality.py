import itertools
import networkit as nk
import logging
import time
logging.basicConfig(level=logging.DEBUG)
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
        nk.traversal.Traversal.BFSfrom(self.G, group, lambda u, dist: distances.append(dist))
        normalized = []
        for dist in distances:
            if(dist != 0):
                normalized.append(1./dist)
            else:
                normalized.append(0.0)

        return sum(normalized)


    def compute_groups_centralities(self):
        logging.debug("Computing all the subsets of %r nodes"%(self.k))
        start_groups = time.time()
        self.groups = self.findsubsets(self.nodes,self.k)
        end_groups = time.time()
        logging.debug("Elapsed time = %r"%(end_groups-start_groups))
        logging.debug("Number of groups = %r"%(len(self.groups)))
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


    def get_GHC_max_group(self):
        return self.GHC_max_group
    def get_max_group(self):
        return self.max_group





class FairGroupHarmonicCentrality(GroupHarmonicCentrality):
    def __init__(self, G,C, k):
        super().__init__(G, k)
        # Fair Group Harmonic Centrality
        self.communities = C
        # Dictionary <key,value> <---- <int,list>
        # key = key is the index of a community
        # value = each index of the list is the index of a subset of k nodes
        self.FGHC = {}

    # Compute the Group Harmonic Centrality between the community and the group
    def HarmonicOfGroupOnSubsets(self,C, group):
        subgraph = nk.subgraphFromNodes(self.G,C)
        distances = []
        nodes = [u for u in subgraph.iterNodes()]
        if(len(set(nodes).intersection(group))>0):
            nk.traversal.Traversal.BFSfrom(subgraph, group, lambda u, dist: distances.append(dist))
            normalized = []
            for dist in distances:
                if (dist != 0):
                    normalized.append(1. / dist)
                else:
                    normalized.append(0.0)
            return sum(normalized)
        else:
            return (0.0)


    # for each community computes all the Fair Group Harmonic Centrality wrt each group of k nodes
    def computeFairGroupHarmonicCentrality(self):
        self.compute_groups_centralities()
        i = 0
        for community in self.communities:
            self.FGHC[i] = []
            for group in self.groups:
                GHC = self.HarmonicOfGroupOnSubsets(community,group)
                if(GHC >0):
                    self.FGHC[i].append(GHC * (1./(len((set(community) - set(group))))))
                else:
                    self.FGHC[i].append(GHC)
            i+=1