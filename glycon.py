'''Class representing Glycon'''

import networkx as nx
import pylab 

class Monomer():

    def __init__(self, carbon_index, shape):
        self.carbonIndex = carbon_index
        self.shape = shape

    def __str__(self):
        return "%s" % id(self)

    def __repr__(self):
        return "%s:%s" % (self.shape, self.carbonIndex)



class Glycon():

    def __init__(self, id, root):
        self.topology = nx.DiGraph()
        self.id = id
        self.shapes = { 'C' : 'circle'
                , 'R' : 'rect'
                , 'T' : 'triangle' }
        self.addNode(root)

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

    def addNode(self, monomer):
        assert isinstance(monomer, Monomer)
        n = self.topology.add_node(monomer
            , label = monomer.__repr__()
            , shape=self.shapes[monomer.shape]
            , carbon_index=monomer.carbonIndex
            )


    def addMonomer(self, monomer, parent = None):
        """Add monomer with optional parent"""
        carbonIndex = monomer.carbonIndex
        shape = monomer.shape
        self.addNode(monomer)
        if parent:
            assert isinstance(parent, Monomer)
            self.topology.add_edge(monomer, parent)


if __name__ == "__main__":

    m1, m2, m3 = Monomer(1, "C"), Monomer(0, "R"), Monomer(1, "T")
    glycan = Glycon("G1", m1)
    glycan.addMonomer(m2)
    glycan.addMonomer(m2)
    glycan.addMonomer(m3, m2)
    #glycan.writeGraphviz()
    nx.write_dot(glycan.topology, "network.dot")
    #nx.draw(glycan.topology)
    #pylab.show()

