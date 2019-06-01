
"""
    This

"""
from formula import Variable, Node
from formula import buildFormula, prepareString
import axiom

import itertools


def leave_uniq(formulas):

    forms = []

    for i in range(len(formulas)):
        if not formulas[i] in forms:
            forms.append(formulas[i])

    formulas = forms

def implication_splitter(tree):

    """
        Splits formula to use |- F->G => F |- G
    :param tree: formula
    :return: F, G
    """

    """
        if formula is like (...) and it's the left child of the tree,
        leave just one side: 
            left = (F->G), right = None
            tree = left
    """

    if type(tree) == Variable:
        return tree, None

    if tree.right is None:
        tree = tree.left

    F = tree.left
    G = tree.right

    return F, G

def formal_output(tree):
    TREES = set()

    initial_tree = tree # i HOPE it will not be reference

    symbols = tree.used_symbols() # set of used symbols
    symbols = list(symbols)




if __name__ == '__main__':

    '''
        (F->G) -> ( (!F->G) -> G)
        
    s = "!A->(A->B)" #input()
    s = "(F->G) -> ( (!F->G) -> G)"
    "((a->b)->a)->a"
    '''

    print('Enter formula:')

    s = input()
    s = prepareString(s)
    s = list(s)
    tree = buildFormula(s)

    print()
    formal_output(tree)