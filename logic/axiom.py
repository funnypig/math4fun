from formula import Variable, Node, notFormula

def deduction(hypothesis, tree):
    """
        Gamma, F |- G   =>  Gamma |- F->G

        hypothesis is a node
    """

    msg = "Deduction theorem for " + str(hypothesis) + ", " + str(tree)

    new_tree = Node(hypothesis, tree, msg=msg)
    return new_tree

def A1(F, G):
    """
        F -> (G -> F)   axiom (1)
    """

    if F is None or G is None:
        return None

    tree = Node(G,F)
    tree = Node(F, tree)

    tree.msg = "A1 for " + str(F) + ", " + str(G)

    return tree

def A2(F, G, H):
    """
        (F -> (G -> H)) -> ( (F -> G) -> (F -> H) )     axiom (2)
    """
    gh = Node(G, H)
    fgh = Node(F, gh)

    fg = Node(F, G)
    fh = Node(F, H)
    fgfh = Node(fg, fh)

    msg = "A2 for " + str(F) + ", " + str(G) + ", " + str(H)

    res = Node(fgh, fgfh, msg=msg)

    return res

def A3(F, G):
    """
        (!G -> !F) -> ( (!G -> F) -> G )    axiom (3)
    """

    try:
        notG = notFormula(G)
        notF = notFormula(F)

        ngnf = Node(notG, notF)

        ngf = Node(notG, F)

        ngf_g = Node(ngf, G)

        msg = "A3 for " + str(F) + ", " + str(G)

        return Node(ngnf, ngf_g, msg=msg)
    except:
        return None


def _MP(F1, F2):
    """
        F, F->G |- G

        F1 = F
        F2 = F->G
    """

    try:
        if F2.left == F1:

            mp_result = F2.right
            mp_result.msg = "MP for " + str(F1) +", " +str(F2)

            return mp_result
    except:
        pass

    return None

def MP(F1, F2):
    f12 = _MP(F1, F2)
    if f12 is None:
        return _MP(F2, F1)

    return f12

def TL(F):

    msg = "L theorem for " + str(F)
    return Node(F, F, msg=msg)

def T3(F,G):
    """
        !F -> (F->G)
    """

    if type(F) is Node:
        nf = Node(F.left, F.right, _not = not F._not)
    else:
        nf = Variable(F.symbol, _not = not F._not)

    fg = Node(F, G)

    msg = "T3 for " + str(F) +", "+str(G)

    return Node(nf, fg, msg=msg)

def T4(F,G):
    """
        (!G->!F) -> (F->G)
    """

    if type(F) is Node:
        nf = Node(F.left, F.right, _not=not F._not)
    else:
        nf = Variable(F.symbol, _not=not F._not)

    if type(G) is Node:
        ng = Node(G.left, G.right, _not=not G._not)
    else:
        ng = Variable(G.symbol, _not=not G._not)

    f1 = Node(ng, nf)
    f2 = Node(F, G)

    msg = "T4 for " + str(F) +", "+str(G)

    return Node(f1, f2, msg=msg)

def T5(F, G):
    """
        (F->G) -> (!G -> !F)
    """

    if type(F) is Node:
        nf = Node(F.left, F.right, _not=not F._not)
    else:
        nf = Variable(F.symbol, _not=not F._not)

    if type(G) is Node:
        ng = Node(G.left, G.right, _not=not G._not)
    else:
        ng = Variable(G.symbol, _not=not G._not)

    f1 = Node(F, G)
    f2 = Node(ng, nf)

    msg = "T5 for " + str(F) +", "+str(G)

    return Node(f1, f2, msg=msg)

def T6(F, G):
    """
        F -> (!G -> !(F->G) )
    """

    if type(G) is Node:
        ng = Node(G.left, G.right, _not=not G._not)
    else:
        ng = Variable(G.symbol, _not=not G._not)

    nFG = Node(F, G, _not=True)

    f2 = Node(ng, nFG)

    msg = "T6 for " + str(F) +", "+str(G)

    return Node(F, f2, msg=msg)

def T7(F,G):
    """
        (F->G) -> ( (!F->G) ->G )
    """

    if type(F) is Node:
        nf = Node(F.left, F.right, _not=not F._not)
    else:
        nf = Variable(F.symbol, _not=not F._not)

    fg = Node(F, G)

    nf_g = Node(nf, G)
    nfg_G = Node(nf_g, G) # (!F->G)->G

    msg = "T7 for " + str(F) +", "+str(G)

    return Node(fg, nfg_G, msg=msg)

def S1(F1, F2):
    """
        F->G, G->H |- F->H

        F1 = F->G
        F2 = G->H
    """
    try:
        if F1.right == F2.left:

            msg = "S1 for " + str(F1) + ", " + str(F2)

            node = Node(F1.right, F2.left, msg=msg)
            return node
    except:
        pass

    return None

def S2(F1, F2):
    """
        F->(G->H), G |- F->H

        F1 = F->(G->H)
        F2 = G
    """

    try:
        msg = "S2 for " + str(F1) + ", " + str(F2)

        if F1.right.left == F2:
            node = Node(F1.left, F1.right.right, msg=msg)

    except:
        pass

    return None

THEOREMS = [T3, T4, T5, T6, T7]

def if_A1(F):
    # F->(G->F)

    try:
        # f1 -> f2
        f1 = F.left
        f2 = F.right

        # f2 has to be equal to: g->f1
        if f2.right == f1:
            return True

    except:
        # F is variable or does not have left or right Node
        pass

    return False


def if_A2(F):
    # (F->(G->H)) -> ((F->G)->(F->H))
    # ___________    ________________
    #      F1               F2

    try:

        F1 = F.left
        F2 = F.right

        F = F1.left
        G,H = F1.right.left, F1.right.right

        if  F2.left.left == F and F2.left.right == G and\
            F2.right.left == F and F2.right.right == H:

            return True

    except:
        # F is variable or does not have left or right Node
        pass

    return False


def if_A3(F):
    # (!B->!A) -> ((!B->A)->B)
    # ________    ____________
    #    F1            F2

    try:
        F1 = F.left
        F2 = F.right

        B = F2.right
        A = F2.left.right

        nB = notFormula(B)
        nA = notFormula(A)

        if F1.left == nB and F1.right == nA and \
            F2 == Node(Node(nB, A), B):

            return True

        a3 = A3(A,B)


        if a3 == F:
            return True

    except:
        # F is variable or does not have left or right Node
        pass

    return False


def if_Axiom(F):
    """
        Check if F is Axiom
    """

    return if_A1(F) or if_A2(F) or if_A3(F)


if __name__ == '__main__':

    f1 = Variable('F')
    f2 = Node(Variable('F'), Variable('G'))
    print(MP(f1,f2))
    exit()


    f1 = "(A->B)"
    f2 = "(A->!(B->!C))"
    tests = [
        "F->(G->F)", "G->(F->G)", "F->(F->F)", "!F->((A->B)->!F)",

        "(A->(B->C))->((A->B)->(A->C))", "({0}->(B->{1}))->(({0}->B)->({0}->{1}))".format(f1,f2),

        "(!G->!F)->((!G->F)->G)", "(!G->!G)->((!G->G)->G)",

        "(!(f1)->!(f2))->((!(f1)->(f2))->(f1))".replace('f1',f1).replace('f2',f2)
    ]

    from formula import prepareString, buildFormula, IncorrectInput

    for t in tests:
        try:
            f = buildFormula(prepareString(t))

            a1 = if_A1(f)
            a2 = if_A2(f)
            a3 = if_A3(f)

            print(t)
            print('axiom A1:',a1)
            print('axiom A2:',a2)
            print('axiom A3:',a3)
            print()

        except IncorrectInput:
            print(t)
            print("Incorrect!")
            print()