import networkit as nk



class FairHarmonicCentrality:

    def __init__(self, G, C, k, TopHarmonicCloseness=None):
        if TopHarmonicCloseness is None:
            self.TopHarmonicCloseness = {"top": True, "useNBbound": False,'normalized':False}
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

    def compute_top_k_fair_group_centrality(self):
        # Computing the fairness level of the first k
        self.S = self.HC.topkNodesList()
        # For each community, get the group centrality of each community wrt the set S
        fairness = []
        for community in self.C:
            group = list(set(community).intersection(set(self.S)))
            if(len(group)>0):
                SG = self.G.subgraphFromNodes(group)
            else:
                fairness.append(0)

        print("Miao")



G = nk.graphio.SNAPGraphReader().read("../datasets/com-youtube/com-youtube.ungraph.txt")
# Kadabra is apx betweennes
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