from src.measures.GroupHarmonicCentrality import GroupHarmonicCentrality
# NEED TO BE DEFINED work in progress
class FairGroupHarmonicCentrality(GroupHarmonicCentrality):
    def __init__(self, G,C, k):
        super().__init__(G, k)
        # Fair Group Harmonic Centrality
        self.FGHC = []
        self.communities = C

    def compue_fair_group_harmonic_centrality(self):
        self.compute_groups_centralities()
        j = 0
        for group in self.groups:
            self.FGHC.append(self.groups_centralities[j] * (1./(len((set(self.nodes) - set(group))))))
            j+=1