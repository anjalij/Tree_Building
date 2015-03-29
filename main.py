import sys
import cell
import parser

def main(ruleFile):
    parser.parse_rulefile(ruleFile)
    c = cell.Cell()
    c.initCell()
    c.simulate()

if __name__ == '__main__':
    ruleFile = sys.argv[1]
    main(ruleFile)
