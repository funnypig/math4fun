
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
import theorem_maker

print('Enter formula:')

s = input()
s = prepareString(s)
s = list(s)
tree = buildFormula(s)

print()

proof = theorem_maker.Ad_Theorem(tree)

file = open('Proof_'+str(tree)+'.txt','w',encoding='utf-8')


file.write("Proof for: "+str(tree)+'\n\n')

index = 0
for p in proof:
    if p is None:continue

    file.write(str(index)+'.\t'+str(p)+'\n'+p.msg+'\n\n')

    index+=1

file.close()

for p in proof[-10:]:
    print(p)
    if not p is None:
        print(p.msg)

    print()