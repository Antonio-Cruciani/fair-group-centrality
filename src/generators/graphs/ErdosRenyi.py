import networkit as nk
from src.generators.graphs.structure.community import community
class ErdosRenyi(community):


    def __init__(self,n,p,communities_number=None,communities_structure="bfs", communities_size = None,treshold = 3):

        if(communities_size != None):
            super().__init__(nk.generators.ErdosRenyiGenerator(n,p).generate(),communities_structure,communities_size,treshold)
        else:
            # Assuming that n/communities_number give us an int
            cs = [n/communities_number for k in range(0,communities_number)]
            super().__init__(nk.generators.ErdosRenyiGenerator(n,p).generate(),communities_structure,cs,treshold)
        self.n = n
        self.p = p

    def get_n(self):
        return self.n
    def get_p(self):
        return self.p

    def save_graph(self,outPath="./"):
        if (outPath[-1] != "/"):
            outPath += "/"
        instance = {
            'outPath': outPath,
            'graph':'Erdos-Renyi',
            'parameters': {
                'P':self.p,
                'Communities':self.k

            }

        }
        self.write_instance(instance)


