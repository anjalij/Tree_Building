'''
Class representing compartments.

Comparment has rules, and molecules (Glycon)

'''

import parser 
import glycan
import numpy as np
import networkx as nx
import StringIO as sio
import re
import copy
import globals as g
import pylab


def equal(children, pattern):
    result = []
    for i, p in enumerate(children): 
        if pattern[i] == 'X':
            result.append(True)
        else:
            result.append(p == pattern[i])
    return sum(result) == len(result)

    
class Compartment():

    def __init__(self, id):
        self.id = id
        self.input = None
        self.output = None
        # Each compartment can have more than one rule, therefore a list.
        self.rules = []
        self.dotText = ""


    def action(self, node, action):
        print("Applying %s at %s" % (action, node))
        parent = self.input.topology[node]
        nodeDict = self.input.topology.node[node]
        action = action.split(',')
        parentShape, cIndices = action[0], action[1:]
        for i, c in enumerate(cIndices):
            if c not in ['_', 'X']:
                m = glycan.Monomer(i, c)
                print("[ACTION] Adding monomer %s" % m)
                self.input.addMonomer(m, node)
                print self.input.topology.nodes()

    def applyRule(self, pattern, output):
        """Apply a single action on input when it satifies given pattern """

        actions = parser.rules[pattern]
        # A pattern may have more than one action in future, select one and apply
        # the action.
        action = np.random.choice(actions)
        print("[INFO] Applying %s: (%s -> %s)" % (self.input, pattern, action))

        pattern = pattern.split(',')
        candidates = []
        for n in self.input.topology.nodes():
            if self.guard(n, pattern):
                candidates.append(n)
        if candidates:
            candidate = np.random.choice(candidates)
            self.action(candidate, action)
        else:
            print("\tNo match for this rule")


    def guard(self, node, pattern):
        nShape, nCIndex = self.input.topology.node[node]['label'].split('_')
        shape, carbonIndices = pattern[0], pattern[1:] 
        if nShape != shape:
            return False

        children = self.input.topology.predecessors(node)
        children.sort(key=lambda x:x.carbonIndex)
        
        if len(children) < len(carbonIndices):
            children += [ '_' for x in range(len(carbonIndices) - len(children))]

        if equal(children, carbonIndices):
            return True
        return False


    def toDot(self):
        if not self.input:
            return ""
        print("Converting input to dot")
        g = nx.to_pydot(self.input.topology)
        content = g.to_string()
        content = re.sub(r'strict(\s+\w+)+\s+{', 'subgraph cluster_%s {' % self.id
                , content
                )
        self.dotText = content
        return content


    def applyRules(self, sim_step):
        if self.input is None:
            print("Warn: Compartment %s has no input" % self.id) 
            return
        np.random.shuffle(self.rules)
        output = copy.deepcopy(self.input)
        for r in self.rules:
            output = self.applyRule(r, output)
        return output 

class Cell():

    def __init__(self):
        self.compartments = []
        self.simSteps = 0
        self.dotText = []

    def initCell(self):
        for i in range(g.num_compartments_):
            # Select rules randomly
            self.compartments.append(Compartment(i))

        # Parse the rules, randomly select few rules and put them in
        # compartment.
        for compt in self.compartments:
            self.addRule(compt)

    def addRule(self, compartment):
        """Add rule to compartments"""
        numRules = np.random.randint(1, g.num_compartments_)
        compartment.rules = np.random.choice(parser.rules.keys(), numRules)

    def step(self):
        for i, c in enumerate(self.compartments):
            if c.input: 
                self.simSteps += 1
                output = c.applyRules(self.simSteps)
                try:
                    self.compartments[(c.id+1)].input = output
                except IndexError:
                    print("No compartment is connected with %s" % c.id)
                self.dotText.append(c.toDot())

    def writeDotFile(self, filename=None):
        dotText = "strict digraph cell {\n"
        dotText += "\n".join(self.dotText)
        dotText += "\n}"
        if not filename:
            print(dotText)
            return
        with open(filename, "w") as f:
            f.write(dotText)

    def simulate(self, steps = -1):
        """Simulate the cell """
        print("Simulating for %s steps" % steps)
        self.compartments[0].input = g.input_
        self.step()
        self.writeDotFile(filename="network.dot")

