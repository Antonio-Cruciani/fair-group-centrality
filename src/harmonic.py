import networkit as nk

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