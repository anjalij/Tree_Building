'''Class representing Glycan'''

import networkx as nx
import pylab 

class Monomer():

    def __init__(self, carbon_index, shape):
        self.carbonIndex = carbon_index
        self.shape = shape

    def __str__(self):
        return "%s" % id(self)

    def __repr__(self):
        return "%s_%s" % (self.shape, self.carbonIndex)



class Glycan():

    def __init__(self, id, root):
        self.topology = nx.DiGraph()
        self.id = id
        self.shapes = { 'C' : 'circle'
                , 'T' : 'triangle' 
                ,  'S' : 'rect'
                }
        self.colors = { 0 : "red", 1 : "blue", 2 : "yellow", 3 : "gray" }
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
        return self.id 

    def display(self):
        nx.draw(self.topology)
        pylab.show()

    def writeGraphviz(self):
        dotFile = '%s.dot' % self.id
        print("Writing topology to %s" % dotFile)
        nx.write_dot(self.topology, dotFile)

    def addNode(self, monomer):
        assert isinstance(monomer, Monomer)
        n = self.topology.add_node(monomer
            , label = monomer.__repr__()
            , shape=self.shapes[monomer.shape]
            , carbon_index=monomer.carbonIndex
            , color=self.colors.get(monomer.carbonIndex, 'black')
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

    m1, m2, m3 = Monomer(1, "C"), Monomer(4, "R"), Monomer(1, "T")
    m4, m5, m6 = Monomer(1, "C"), Monomer(0, "R"), Monomer(1, "T")
    glycan = Glycan("G1", m1)
    glycan.addMonomer(m2, m1)
    glycan.addMonomer(m3, m1)
    glycan.addMonomer(m4, m1)
    glycan.addMonomer(m5, m4)
    glycan.addMonomer(m6, m5)
    children = glycan.topology.predecessors(m1)
    print children
    children.sort(key=lambda x: x.carbonIndex)
    print children
    #glycan.writeGraphviz()
    nx.write_dot(glycan.topology, "network.dot")
    #nx.draw(glycan.topology)
    #pylab.show()

