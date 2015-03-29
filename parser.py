import re
import sys
import os
from collections import defaultdict

# This dictionary keeps all the rules from rules.txt file. Key is condition, and
# value associated with key is action.
rules = defaultdict(list)

def parse_rulefile(rule_file):
    '''Parse the rule file'''
    print("Parsing rule file: %s" % rule_file)
    with open(rule_file, "r") as rF:
        for line in rF:
            line = line.strip()
            if not line: continue
            if line[0] == "#": continue
            condition, action = line.split("->")
            rules[condition.strip()].append(action.strip())
