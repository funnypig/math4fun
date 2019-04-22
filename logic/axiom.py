from formula import Variable, Node

def make_formal(tree):
    pass


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

    tree = Node(F, G)
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

    return Node(fgh, fgfh, msg=msg)

def A3(F, G):
    """
        (!G -> !F) -> ( (!G -> F) -> G )    axiom (3)
    """

    try:
        notG = Node(G.left, G.right, _not = not G._not) if type(G) is Node else Variable(G.symbol, _not= not G._not)
        notF = Node(F.left, F.right, _not = not F._not) if type(F) is Node else Variable(F.symbol, _not= not F._not)

        ngnf = Node(notG, notF)

        ngf = Node(notG, F)

        ngf_g = Node(ngf, G)

        msg = "A3 for " + str(F) + ", " + str(G)

        return Node(ngnf, ngf_g, msg=msg)
    except:
        return None


def MP(F1, F2):
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
