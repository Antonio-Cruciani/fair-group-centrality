import networkit as nk
import random
from measures.GroupHarmonicCentrality import GroupHarmonicCentrality,FairGroupHarmonicCentrality
from generators.graphs.ErdosRenyi import ErdosRenyi
from generators.graphs.BarabasiAlblert import BarabasiAlbert
from generators.graphs.SBM import SBM
sizes = [10,10,10,10,10]
n = 50
p = 0.5
k = 3
ba =  BarabasiAlbert(n, k,communities_number = 50,communities_structure = "BFS",communities_size = sizes)
ba.run()

print("Detected")
ba.communityDetection('plm')

print(ba.get_detectedCommunities())
print("Syntetic")
print(ba.get_communities())
er = ErdosRenyi(n,p,communities_number = 50,communities_structure = "BFS",communities_size = sizes)
er.run()
print("ERDOS")
print("Detected")
er.communityDetection("plm")
print(er.get_detectedCommunities())
print("Syntetic")
print(er.get_communities())
n = 500
k = 10
p_in = 0.7
p_out = 0.4
sbm = SBM(n,p_in,p_out,k)
print("SBM")
print(sbm.get_communities())


exit(1)

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
n = 500
k = 10
p_in = 0.7
p_out = 0.4
Clustered = nk.generators.ClusteredRandomGraphGenerator(n,k,p_in,p_out)
clustered = Clustered.generate()
C =  Clustered.getCommunities()
idCommunities =  C.getSubsetIds()
Communities = []
for id in idCommunities:
    Communities.append(list(C.getMembers(id)))

nodi = [u for u in clustered.iterNodes()]
S= [random.sample(nodi, k)]


exit(1)
GH = GroupHarmonicCentrality(clustered,k)
#GH.sampleS(150)
GH.samplePageRankS()
GH.computeGroupsCentralities()
print("ALL SAMPLES group - centrality")
print(GH.get_groups())
print(GH.get_groups_centralities())
print("--------------------------")
print("GH max group: ",GH.get_max_group() )
print("GH Value :",GH.get_GHC_max_group())
FGH = FairGroupHarmonicCentrality(clustered,Communities,10)
FGH.samplePageRankS(50)
FGH.computeGroupsCentralities()

#FGH.computeFairGroupHarmonicCentrality([GH.get_max_group()] )
FGH.sampleInEachCommunity()
FGH.computeFairGroupHarmonicCentrality()
print(FGH.get_S())
OverallHarmonic = FGH.get_max_group()
print("FGHC of S ",FGH.get_FGHC())
print("overall HC of S ",OverallHarmonic)


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