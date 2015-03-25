'''Class representing Glycon'''

import networkx as nx
import pylab 

class Glycon():

    def __init__(self):
        self.name = None
        self.topology = nx.DiGraph()

    def num_monomers(self):
        return self.topology.number_of_nodes()

    def edgesBetween(self, parent_shape, child_shape, carbon_index):
        edges = []
        for e in self.topology.edges():
            child, parenet = e
            carbonIndex = self.topology.edges[e]['carbon_index']
            childShape = self.topology.nodes[child]['shape']
            parentShape = self.topology.nodes[parent]['shape']
            if carbon_index == carbonIndex:
                if child_shape == childShape:
                    if parent_shape == parentShape:
                        edges.append(e)
            return edges

    def isUniqueEdgeBetween(self, parent_shape, child_shape, carbon_index):
        edges = len(edgesBetween(parent_shape, child_shape, carbon_index))
        if len(edges) == 1:
            return True
        elif len(edges) == 0:
            print("+ WARNING: No edge is found between these shapes")
            print("|- Child: %s -> Parent: %s " % (child_shape, parent_shape))
            return False
        return False
        

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

