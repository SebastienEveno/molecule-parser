[![Build Status](https://travis-ci.com/SebastienEveno/molecule-parser.svg?branch=master)](https://travis-ci.com/SebastienEveno/molecule-parser)

# Chemical Formula Parser
This code can be used to parse chemical formulas (as strings).

## Python required version
The required Python version is 3.9.
Local python version:
```
python --version
```
## Example
### Al<sub>2</sub>(SO<sub>4</sub>)<sub>3</sub>
`"Al2(SO4)3"` will give `{'Al': 2, 'S': 3, 'O': 12}`.