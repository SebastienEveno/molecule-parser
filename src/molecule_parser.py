"""A class that can be used to represent a chemical formula parser."""

from src.atom import Atom
from src.molecule import Molecule
import re # for re.findall()

# we use Regular Expression (RegEx) module to parse the chemical formula
# see https://www.w3schools.com/python/python_regex.asp

class MoleculeParserError(Exception):
    """Base class for other exceptions."""
    pass

class EmptyMoleculeString(MoleculeParserError):
    """Raised when empty chemical formula."""
    def __init__(self, message: str = "The chemical formula is empty!") -> None:
        self.message = message
        super().__init__(self.message)
    
class BracketsNotOk(MoleculeParserError):
    """Raised when brackets are missing in chemical formula."""
    def __init__(self, message: str = "Missing brackets in chemical formula!") -> None:
        self.message = message
        super().__init__(self.message)

class hasNoLetters(MoleculeParserError):
    """Raised when there is no letters in chemical formula."""
    def __init__(self, message: str = "No letter in chemical formula!") -> None:
        self.message = message
        super().__init__(self.message)

class hasEmptyBrackets(MoleculeParserError):
    """Raised when there are any empty brackets in the chemical formula."""
    def __init__(self, message: str = "Empty brackets in chemical formula!") -> None:
        self.message = message
        super().__init__(self.message)

class SpecialCharactersInString(MoleculeParserError):
    """Raised when special character in chemical formula."""
    
    def __init__(self, ind: list = None, formula: str = "", message: str = "Special(s) character(s)") -> None:
        if ind is not None:
            self.ind = ind
        else:
            self.ind = []
        self.spec_char = [formula[i] for i in ind]
        self.message = message
        super().__init__(self.message + " {} at index(es) {}.".format(self.spec_char, self.ind))

class MoleculeParser:
    """
    A parser class to parse chemical formulas as strings.

    Attributes
    ----------
    opening_brackets_type: str, optional
        The type of opening brackets allowed in the chemical formula.
    closing_brackets_type: str, optional
        The type of closing brackets allowed in the chemical formula.
    
    Methods
    ----------
    areBracketsOk(molecule_str: str):
        Check if brackets are missing in the chemical formula.
    hasSpecialCharacters(molecule_str: str):
        Return True if there is any special character in the chemical formula and their indexes.
    hasLetters(molecule_str: str):
        Return True if there are letters in the chemical formula.
    hasEmptyBrackets(molecule_str: str):
        Return True if there are any empty brackets in the chemical formula.
    parse(molecule_str: str):
        Parse the chemical formula.
    """

    def __init__(self, opening_brackets_type: str = "([{", 
            closing_brackets_type: str = ")]}") -> None:
        """Initialize the molecule parser's attributes."""
        self.opening_brackets_type = opening_brackets_type
        self.closing_brackets_type = closing_brackets_type


    def areBracketsOk(self, molecule_str: str) -> bool:
        """Check if brackets are missing in the chemical formula."""
        c_round_brackets = 0
        c_square_brackets = 0
        c_curly_brackets = 0
        for i in molecule_str:
            if i == "(":
                c_round_brackets += 1
            elif i == ")":
                 c_round_brackets -= 1
            elif i == "[":
                c_square_brackets += 1
            elif i == "]":
                c_square_brackets -= 1
            elif i == "{":
                c_curly_brackets += 1
            elif i == "}":
                c_curly_brackets -= 1
            if c_round_brackets < 0 or c_square_brackets < 0 or c_curly_brackets < 0:
                return False
        return (c_round_brackets == 0 and c_square_brackets == 0 and c_curly_brackets == 0)

    def hasSpecialCharacters(self, molecule_str: str) -> tuple[bool, list]:
        """Return True if there is any special character in the chemical formula and their indexes."""
        special_characters = " !\"#$%&\'*+,-./:;<=>?@\\^_`~|"
        ind = [ch in special_characters for ch in molecule_str]
        return any(ind), [i for i, x in enumerate(ind) if x]
    
    def hasLetters(self, molecule_str: str) -> bool:
        """Return True if there are letters in the chemical formula."""
        return molecule_str.lower().islower()

    def hasEmptyBrackets(self, molecule_str: str) -> bool:
        """Return True if there are any empty brackets in the chemical formula."""
        ind = 0
        while ind < len(molecule_str) - 1:
            ch = molecule_str[ind]
            if ch in self.opening_brackets_type and molecule_str[ind + 1] in self.closing_brackets_type:
                return True
            ind += 1
        return False
    
    def parse(self, molecule_str: str) -> dict:
        """
        Parse the chemical formula.
        Return a dictionary of the atoms that make the molecule.
        """
        if not molecule_str:
            raise EmptyMoleculeString()
        
        if not (self.areBracketsOk(molecule_str)):
            raise BracketsNotOk()
        
        hasSpecialCharactersInString, ind = self.hasSpecialCharacters(molecule_str)
        if (hasSpecialCharactersInString):
            raise SpecialCharactersInString(ind=ind, formula=molecule_str)

        if not (self.hasLetters(molecule_str)):
            raise hasNoLetters()
        
        if self.hasEmptyBrackets(molecule_str):
            raise hasEmptyBrackets()
        
        # at this point, the chemical formula makes sense to be parsed.
        # https://codereview.stackexchange.com/questions/232630/parsing-molecular-formula

        molecule_tokens = re.findall("[A-Z][a-z]?|\\d+|.", molecule_str)
        
        isPreviousTokenAClosingParenthesis = False
        isPreviousAnAlpha = False
        list_submolecules = []
        final_molecule = Molecule()

        for ind, token in enumerate(molecule_tokens):
            if token.isalpha():
                if isPreviousAnAlpha:
                    if list_submolecules:
                        list_submolecules[-1].addAtom(atom)
                    else:
                        final_molecule.addAtom(atom)
                    isPreviousAnAlpha = False
                
                if isPreviousTokenAClosingParenthesis:
                    if len(list_submolecules) == 1:
                        final_molecule.addSubmolecule(list_submolecules[-1])
                    else:
                        # add the lowest submolecule to the upper one
                        list_submolecules[-2].addSubmolecule(list_submolecules[-1])
                    
                    # remove the lowest submolecule from the list
                    list_submolecules = list_submolecules[:-1]

                    isPreviousTokenAClosingParenthesis = False
                
                atom = Atom(token)
                isPreviousAnAlpha = True

                # if we are at the end of the list, add atom
                if ind == len(molecule_tokens) - 1:
                    final_molecule.addAtom(atom)

            elif token.isdecimal():
                c = int(token)
                isPreviousAnAlpha = False
                
                # Case first token is number. Example: "3(H20)"
                if ind == 0:
                    final_molecule.number = c
                
                elif isPreviousTokenAClosingParenthesis:
                    # Number corresponds to the lowest submolecule
                    # Here len(list_submolecules) >= 1
                    list_submolecules[-1].number = c
                    # at this point, we can add this submolecule to the upper one,
                    # or add it to final_molecule if len(list_submolecules) == 1
                    if len(list_submolecules) == 1:
                        final_molecule.addSubmolecule(list_submolecules[-1])
                    else:
                        # add the lowest submolecule to the upper one
                        list_submolecules[-2].addSubmolecule(list_submolecules[-1])
                    
                    # remove the lowest submolecule from the list
                    list_submolecules = list_submolecules[:-1]

                    isPreviousTokenAClosingParenthesis = False
                else:
                    # Number corresponds to atom
                    atom.number = c
                    if list_submolecules:
                        list_submolecules[-1].addAtom(atom)
                    else:
                        final_molecule.addAtom(atom)

            elif token in self.opening_brackets_type:
                if isPreviousAnAlpha:
                    if list_submolecules:
                        list_submolecules[-1].addAtom(atom)
                    else:
                        final_molecule.addAtom(atom)
                    isPreviousAnAlpha = False
                
                # case previous token in ")]}", i.e. in closing brackets
                if isPreviousTokenAClosingParenthesis:
                    if len(list_submolecules) == 1 or ind == len(molecule_tokens) - 1:
                        final_molecule.addSubmolecule(list_submolecules[-1])
                    else:
                        # add the submolecule to the upper submolecule
                        list_submolecules[-2].addSubmolecule(list_submolecules[-1])
                    
                    # remove the lowest submolecule from the list
                    list_submolecules = list_submolecules[:-1]

                    isPreviousTokenAClosingParenthesis = False
                
                # add new submolecule to list_submolecules
                list_submolecules.append(Molecule())

            elif token in self.closing_brackets_type:
                if isPreviousAnAlpha:
                    if list_submolecules:
                        list_submolecules[-1].addAtom(atom)
                    else:
                        final_molecule.addAtom(atom)
                    isPreviousAnAlpha = False
                
                if isPreviousTokenAClosingParenthesis:
                    if len(list_submolecules) == 1 or ind == len(molecule_tokens) - 1:
                        final_molecule.addSubmolecule(list_submolecules[-1])
                    else:
                        # add the submolecule to the upper submolecule
                        list_submolecules[-2].addSubmolecule(list_submolecules[-1])
                    
                    # remove the lowest submolecule from the list
                    list_submolecules = list_submolecules[:-1]
                
                # case this closing bracket is the last element of the string
                elif ind == len(molecule_tokens) - 1:
                    final_molecule.addSubmolecule(list_submolecules[-1])
                
                isPreviousTokenAClosingParenthesis = True
        
        return final_molecule.getAtomsAsDict()

