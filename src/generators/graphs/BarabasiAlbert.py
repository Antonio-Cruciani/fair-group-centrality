import networkit as nk
from src.generators.graphs.structure.community import community

class BarabasiAlbert(community):

    def __init__(self,n,k,communities_number,communities_structure, communities_size = None,treshold=None):

        if(communities_size != None):
            super().__init__(nk.generators.BarabasiAlbertGenerator(k,n).generate(),communities_structure,communities_size,treshold)
        else:
            # Assuming that n/communities_number give us an int
            cs = [n/communities_number for k in range(0,communities_number)]
            super().__init__(nk.generators.ErdosRenyiGenerator(k,n).generate(),communities_structure,cs,treshold)
        self.n = n
        self.k = k

    def get_n(self):
        return self.n
    def get_k(self):
        return self.k

    def save_graph(self,outPath="./"):
        if(outPath[-1] != "/"):
            outPath+="/"
        instance = {
            'outPath':outPath,
            'graph':'Barabasi-Albert',
            'parameters': {
                'Max_degree':self.k,
                'Communities':len(self.get_communities()),

            }

        }
        self.write_instance(instance)



