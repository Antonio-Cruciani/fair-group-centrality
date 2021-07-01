import itertools
from src.generators.graphs.SBM import SBM
from src.generators.graphs.ErdosRenyi import ErdosRenyi
from src.generators.graphs.BarabasiAlbert import BarabasiAlbert
class Harmonic:

    #instance= {
        # type = "Syntetic or Real"
        # graphs = [{ "name": , "parameters":{" "}   }]


    # }
    def __init__(self,instance):

        self.instance = instance


    def run(self):

        if(self.instance['type'] in ['syntetic','Syntetic']):
            self.runSynteticExperiments()

    def runSynteticExperiments(self):

        for elem in self.instance['graphs']:


            listOfParameters = []

            for parameter in self.instance['graphs'][elem]:

                listOfParameters.append(parameter)

            parametersCombination =list(itertools.product(*listOfParameters))

            if(elem in ['Erdos-Renyi','ER','er','Erdos Renyi','ErdosRenyi']):
                print("ciao")
            elif(elem in ['Barabasi-Albert','BA','ba','BarabasiAlbert','Barabasi Albert']):
                print("ciao")

            elif(elem in ['SBM','sbm']):

                print("ciao")


