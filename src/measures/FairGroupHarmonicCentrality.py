from src.measures.GroupHarmonicCentrality import GroupHarmonicCentrality
import networkit as nk

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
            nk.traversal.Traversal.BFSfrom(subgraph, group, lambda u, dist: distances.append(1. / dist))
            return sum(distances)
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