'''
Class representing compartments.

Comparment has rules, and molecules (Glycon)

'''

import parser 
import glycan
import numpy as np
import networkx as nx
import cStringIO as sio
import globals as g

class Compartment():

    def __init__(self, id):
        self.id = id
        self.input = None
        self.output = None
        # Each compartment can have more than one rule, therefore a list.
        self.rules = []
        self.buff = sio.StringIO()

    def actions(self):
        pass

    def applyRule(self, rule, output):
        """Apply a single rule on input """
        actions = parser.rules[rule]

        # A rule may have more than one action in future, select one and apply
        # the action.
        action = np.random.choice(actions)
        print("[INFO] Applying %s: (%s -> %s)" % (self.input, rule, action))

    def dotFile(self):
        if not self.input:
            return ""
        nx.write_dot(self.input.topology, self.buff)
        content = self.buff.getvalue()
        print content


    def applyRules(self, sim_step):
        if self.input is None:
            print("Warn: Compartment %s has not input" % self.id) 
            return
        np.random.shuffle(self.rules)
        output = None
        for r in self.rules:
            self.applyRule(r, output)
        return output 

class Cell():

    def __init__(self):
        self.compartments = []
        self.simSteps = 0

    def initCell(self):
        for i in range(g.num_compartments_):
            # Select rules randomly
            self.compartments.append(Compartment(i))

        # Parse the rules, randomly select few rules and put them in
        # compartment.
        for compt in self.compartments:
            self.addRule(compt)
            compt.dotFile()


    def addRule(self, compartment):
        """Add rule to compartments"""
        numRules = np.random.randint(1, g.num_compartments_)
        compartment.rules = np.random.choice(parser.rules.keys(), numRules)

    def step(self):
        compartmentsWithInput = []
        for i, c in enumerate(self.compartments):
            if c.input: 
                self.simSteps += 1
                output = c.applyRules(self.simSteps)
                self.compartments[i+1].input = output



    def simulate(self, steps = -1):
        """Simulate the cell """
        print("Simulating for %s steps" % steps)
        input =  g.input_
        self.compartments[0].input = input
        self.step()

