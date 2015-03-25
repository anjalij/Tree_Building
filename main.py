import sys
import parser 

def main(ruleFile):
    parser.parse_rulefile(ruleFile)
    print parser.rules


if __name__ == '__main__':
    ruleFile = sys.argv[1]
    main(ruleFile)
