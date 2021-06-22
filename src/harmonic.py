import networkit as nk
from measures.GroupHarmonicCentrality import GroupHarmonicCentrality,FairGroupHarmonicCentrality


class FairHarmonicCentrality:

    def __init__(self, G, C, k, TopHarmonicCloseness=None):
        if TopHarmonicCloseness is None:
            self.TopHarmonicCloseness = {"top": True, "useNBbound": False,'normalized':True}
        else:
            self.TopHarmonicCloseness = TopHarmonicCloseness
        self.G = G
        self.C = C
        self.k = k
        self.HC = None
        # Group Harmonic Centrality and Fair Group Harmonic Centrality
        self.S = None
        self.GHC = None
        self.FGHC = None

    def compute_centrality(self):
        #Compute the Centrality measure
        if(self.TopHarmonicCloseness['top']):

            self.HC  = nk.centrality.TopHarmonicCloseness(self.G,self.k,useNBbound= self.TopHarmonicCloseness['useNBbound'])
        else:
            #Computing centrality exhaustively
            self.HC = nk.centrality.HarmonicCloseness(self.G,normalized= self.TopHarmonicCloseness['normalized'],)
        self.HC.run()

    def computeTopKFairGroupCentrality(self):
        # Computing the fairness level of the first k
        self.S = self.HC.topkNodesList()
        # For each community, get the group centrality of each community wrt the set S
        fairness = []
        for community in self.C:
            group = list(set(community).intersection(set(self.S)))
            if(len(group)>0):
                SG = self.G.subgraphFromNodes(group)
                # Need to define Harmonic Centrality

            else:
                fairness.append(0)




G = nk.graphio.SNAPGraphReader().read("../datasets/dblp/com-dblp.ungraph.txt")
communities = []
with open("../datasets/dblp/com-dblp.all.cmty.txt", 'r') as f:
    data =f.read()

    for line in data.split("\n"):
        community = []
        for elem in line.split("\t"):
            community.append(int(elem))
        communities.append(community)

   # perform file operations
# Kadabra is apx betweennes
GH = GroupHarmonicCentrality(G,10)
GH.compute_groups_centralities()
print("Group with highest group harmonic centrality ",GH.get_max_group())
print("HC of such group",GH.get_GHC_max_group())
exit(1)


exit(1)
kadabra = nk.centrality.KadabraBetweenness(G,0.05,0.8)
kadabra.run()
# The exhaustive Harmonic is really expensive and slow on big graphs,
# Top Harmonic is an apx version that finds only the top k = 10 nodes
harmonic = nk.centrality.TopHarmonicCloseness(G,10,useNBbound= False)
harmonic.run()
print("HARMONIC")
print(harmonic.topkNodesList())
print(harmonic.topkScoresList())
print("KADABRA")
print(kadabra.ranking()[:10])