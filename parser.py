import json
import sys
from src.molecule_parser import MoleculeParser

if __name__ == "__main__":
    
    read_from_stdin = False
    json_output_format = False
    formulas = []
    for arg in sys.argv[1:]:
        if arg.lower() == '-i':
            read_from_stdin = True
        if arg.lower() == '-j':
            json_output_format = True
    
    mp = MoleculeParser()
    if read_from_stdin:
        formulas = list(map(lambda line: line.rstrip(), sys.stdin.readlines()))
    
    if json_output_format:
        print(json.dumps(list(map(lambda formula: mp.parse(formula), formulas)), sort_keys=True, indent=4))
    else:
        for formula in formulas:
            print(mp.parse(formula))