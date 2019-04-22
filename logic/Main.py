
"""
    The goal of this module is to:
        - check if formula of propositional calculus is tautology
        - build formal illation of the given formula

    Variable symbols: capital english letters (A-Z)

    Operations:
        - '!' logical not
        - '->' implication

    Technical symbols: '(', ')'

    Author: Antipiev Illya,

            Faculty of Mechanics and Mathematics,
            Taras Shevchenko National university of Kyiv

            ilya.antipiev@gmail.com
"""


from formula import *
from formal_maker import formal_output

print('Enter formula:')

s = input()
s = prepareString(s)
s = list(s)
tree = buildFormula(s)

print()
formal_output(tree)