'''Class representing Glycon'''

import networkx as nx
import pylab 

class Glycon():

    def __init__(self):
        self.name = None
        self.topology = nx.DiGraph()

    def __repr__(self):
        return self.name 

    def display(self):
        nx.draw(self.topology)
        pylab.show()

    def writeGraphviz(self):
        dotFile = '%s.dot' % self.name
        print("Writing topology to %s" % dotFile)
        nx.write_dot(self.topology, dotFile)

    def add_monomer(self, monomer, parent = None, **kwargs):
        carbonIndex = kwargs.get('carbon_index', -1)
        if not parent:
            self.topology.add_node(monomer)
        else:
            self.topology.add_edge(monomer, parent, carbon_index=carbonIndex
                    , label = carbonIndex
                    )


if __name__ == "__main__":

    glycan = Glycon()
    glycan.name = "G1"
    print glycan
    glycan.add_monomer('P0')
    glycan.add_monomer('P1', 'P0', carbon_index = -1)
    glycan.add_monomer('P1', 'P2', carbon_index = 0)
    glycan.writeGraphviz()

