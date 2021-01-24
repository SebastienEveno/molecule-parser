[![Build Status](https://travis-ci.com/SebastienEveno/molecule-parser.svg?branch=master)](https://travis-ci.com/SebastienEveno/molecule-parser)

# Chemical formula parser
This code can be used to parse chemical formulas (as strings).

## Example
Al<sub>2</sub>(SO<sub>4</sub>)<sub>3</sub> will give:
```
{'Al': 2, 'S': 3, 'O': 12}
```