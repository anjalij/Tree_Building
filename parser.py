import re
import sys
import os

# This dictionary keeps all the rules from rules.txt file. Key is condition, and
# value associated with key is action.
rules = {}

def parse_rulefile(rule_file):
    '''Parse the rule file'''
    print("Parsing rule file: %s" % rule_file)
    with open(rule_file, "r") as rF:
        for line in rF:
            line = line.strip()
            if not line: continue
            condition, action = line.split("->")
            rules[condition] = action
