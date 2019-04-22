
from formula import Variable, Node
from formula import buildFormula, prepareString
import axiom

import itertools

def leave_uniq(formulas):
    i = 0

    while i<len(formulas):
        j = i+1
        while j<len(formulas):
            if formulas[i] == formulas[j]:
                formulas.pop(j)
            else:
                j+=1

        i+=1


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
    initial_tree = tree # i HOPE it will not be reference

    variables = tree.used_symbols() # set of used symbols
    variables = [Variable(v) for v in variables]


    hypoth = []

    # MAKE THEOREMS WITH VARIABLES

    for i in range(len(variables)):
        hypoth.append(axiom.TL(variables[i]))
        nv = Variable(variables[i].symbol, _not = not variables[i]._not)
        hypoth.append(axiom.TL(nv))

        for j in range(len(variables)):
            for T in axiom.THEOREMS:
                hypoth.append(T(variables[i], variables[j]))

    # SAVE FOR DEDUCTION
    for_deduction = []

    splitable = True

    while splitable:
        print("Try to split formula to use Deduction theorem for:",str(tree))
        F, G = implication_splitter(tree)

        if G is None:
            splitable = False
            print("can't split formulas.")
            print()
        else:

            F.msg = "for deduction"
            for_deduction.append(F)
            tree = G

            print("Split used, now we have:")
            print("hypotheses:", '; '.join([str(h) for h in for_deduction]))
            print("formula to get:", str(G))
            print()


    print()
    print("Now we have just to found", str(tree),'\n')

    hypoth.extend(for_deduction)

    leave_uniq(hypoth)

    def use_mp(): # USE Modus Ponens for hypotheses
        nonlocal hypoth

        new_forms = []

        for i in range(len(hypoth)):
            for j in range(len(hypoth)):
                mp = axiom.MP(hypoth[i], hypoth[j])

                if not mp is None:
                    new_forms.append(mp)

                mp = axiom.MP(hypoth[j], hypoth[i])

                if not mp is None:
                    new_forms.append(mp)

        leave_uniq(new_forms)

        return new_forms

    def use_S():
        nonlocal hypoth

        new_forms = []

        for i in range(len(hypoth)):
            for j in range(len(hypoth)):
                s1 = axiom.S1(hypoth[i], hypoth[j])
                s2 = axiom.S2(hypoth[i], hypoth[j])

                if not s1 is None:
                    new_forms.append(s1)
                if not s2 is None:
                    new_forms.append(s2)

                s1 = axiom.S1(hypoth[j], hypoth[i])
                s2 = axiom.S2(hypoth[j], hypoth[i])

                if not s1 is None:
                    new_forms.append(s1)
                if not s2 is None:
                    new_forms.append(s2)

        leave_uniq(new_forms)

        return new_forms

    FOUND = False

    while not FOUND:
        new_forms = []

        new_forms.extend(use_mp())
        new_forms.extend(use_S())

        hypoth.extend(new_forms)

        leave_uniq(hypoth)

        for h in hypoth:
            if h == tree:
                tree = h
                FOUND = True
                break


    print("Formulas:")
    for i in range(len(hypoth)):
        print('{}. {}\t\t{}'.format(i+1,
                                  str(hypoth[i]),
                                  hypoth[i].msg))

    print()
    print("Use deduction theorem:")
    while len(for_deduction)!=0:
        new_tree = axiom.deduction(for_deduction.pop(), tree)

        print(new_tree, "\t\t", new_tree.msg)

        tree = new_tree

if __name__ == '__main__':

    '''
        (F->G) -> ( (!F->G) -> G)
        
    s = "!A->(A->B)" #input()
    s = "(F->G) -> ( (!F->G) -> G)"
    '''

    print('Enter formula:')

    s = input()
    s = prepareString(s)
    s = list(s)
    tree = buildFormula(s)

    print()
    formal_output(tree)