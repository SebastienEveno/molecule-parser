[![Build Status](https://travis-ci.com/SebastienEveno/molecule-parser.svg?branch=master)](https://travis-ci.com/SebastienEveno/molecule-parser)

# Chemical Formula Parser
This Python code can be used to parse chemical formulas, from string input format to a dictionary.

## Required Python version
The required Python version is 3.9.

Local Python version:
```
python --version
```

## Use

Use the command line `python main.py -i` to read from user input.
You can add as many chemical formulas, line by line.
Use `^Z` (ctrl +Z) to escape the input command.

## Examples

### Fe<sub>2</sub>O<sub>3</sub>

```
> python main.py -i
Fe2O3
^Z
```
returns
```
{'Fe': 2, 'O': 3}
```
### (NH<sub>4</sub>)<sub>2</sub>HPO<sub>4</sub>

```
> python main.py -i
(NH4)2HPO4
^Z
```
returns
```
{'H': 9, 'P': 1, 'O': 4, 'N': 2}
```
### Mg<sub>2</sub>[CH<sub>4</sub>{NNi<sub>2</sub>(Li<sub>2</sub>O<sub>4</sub>)<sub>5</sub>}<sub>14</sub>]<sub>3</sub>

```
> python main.py -i
Mg2[CH4{NNi2(Li2O4)5}14]3
^Z
```
returns
```
{'Mg': 2, 'C': 3, 'H': 12, 'N': 42, 'Ni': 84, 'Li': 420, 'O': 840}
```
