
import axiom
from axiom import MP
from formula import Variable, Node, notFormula

def build_TL(F):
    """
        Make L theorem with F

    :param F: Variable or Node
    :return: list of formal conclusions to get F->F
    """

    ff = Node(F, F)
    # A2 for F, F->F, F
    F1 = axiom.A2(F, ff, F)

    # A1 for F, F->F
    F2 = axiom.A1(F, ff)

    # MP for F1 and F2
    F3 = axiom.MP(F2, F1)

    # A1 for F and F
    F4 = axiom.A1(F, F)

    # MP for F3, F4
    F5 = axiom.MP(F3, F4)

    return [F1, F2, F3, F4, F5]

def build_deduction(hypoth, F, G):
    """
        hypoth, F |- G => hypoth |- F->G

        hypoth = {F1, ..., Fn}
        F = Fn
    """

    res = []

    if G==F:
        res = build_TL(F)
    elif axiom.if_Axiom(F) or F in hypoth:

        # A1 for F, G
        F1 = axiom.A1(F, G)
        # MP for F and F1
        F2 = axiom.MP(F, F1)

        res = [F1, F2]

    else:
        s = -1
        r = -1

        for i in range(len(hypoth)):
            for j in range(len(hypoth)):
                # Fs = Fr -> F
                f = Node(hypoth[i], F)
                if hypoth[j] == f:
                    r = i
                    s = j
                    break

            if s!=-1: break

        if s == -1: return None # if happened, it's trouble

        Fs = Node(hypoth[r], F)

        # A2 for G, Fr, F
        F1 = axiom.A2(G, hypoth[s], F)

        # MP for F1, G->Fs
        F2 = axiom.MP(F1, Node(G, Fs))

        # MP for G->Fr, F2
        F3 = axiom.MP(Node(G, hypoth[r]), F2)


        return [F1, F2, F3]

    return res

def syl_1(F, G):
    F1 = F.left

    F4 = MP(F1, F)
    F5 = MP(F4, G)

    res = [F, G, F1, F4]
    res.extend(build_deduction(res, F1, Node(F1, F5)))

def syl_2(F, G):
    # A->(B->C), B |- A->C

    F3 = F.left # A
    F4 = MP(F, F3) # B->C
    F5 = MP(G, F4) # C

    f = build_deduction(F3, F5) # A->C

    res = [F3, F4, F5]
    res.extend(f)

    return res

def build_T7(F,G):
    nF = notFormula(F)

    t7 = Node(
        Node(F, G),
        Node(Node(nF, G),G)
    )
    t7.msg = "T7 for F, G. proof not implemented"

    return [t7]

def build_T1(F):
    nF = notFormula(F)

    F1 = axiom.A3(nF, F)

    f2 = build_TL(nF)
    F2 = f2[-1]

    f3 = syl_2(F1, F2)
    F3 = f3[-1]

    nnF = notFormula(nF)
    F4 = axiom.A1(nnF, nF)

    f5 = syl_1(F4, F3)
    F5 = f5[-1]

    res = [F1]
    res.extend(f2)
    res.extend(f3)
    res.extend([F4])
    res.extend(f5)

    return res

def build_T2(F):
    nF = notFormula(F) # !F
    nnF = notFormula(nF) # !!F
    nnnF = notFormula(nnF) # !!!F

    F1 = axiom.A3(F, nnF) # (!!!F->!F)->((!!F->F)->!!F)

    f2 = build_T1(F) # build th. 1
    F2 = f2[-1] # !!!A->!A

    F3 = MP(F2, F1) # ...->!!A
    F4 = axiom.A1(F, nnnF) # A->...

    f5 = syl_1(F4, F3) # f5[-1] = A->!!A

    res = [F1]
    res.extend(f2)
    res.extend([F3, F4])
    res.extend(f5)

    return res

def build_T3(F, G):
    # !f -> (f->G)
    F1 = notFormula(F)
    F2 = F

    F3 = axiom.A1(F2, F1)
    F4 = MP(F2, F3)

    F5 = axiom.A1(F1, notFormula(G))
    F6 = MP(F1, F3)
    F7 = axiom.A3(F,G)
    F8 = MP(F6, F7)
    F9 = MP(F4, F8)

    hypoth = [F1, F2, F3, F4, F5, F6, F7, F8, F9]

    ded1 = build_deduction(hypoth, F, G)
    ded2 = build_deduction(hypoth+ded1, F1, ded1[-1])

    proof = [F3, F4, F5, F6, F7, F8, F9]
    proof.extend(ded1)
    proof.extend(ded2)

    return proof


def build_T4(F, G):
    # (!G->!F)->(F->G)

    nF = notFormula(F)
    nG = notFormula(G)

    F1 = Node(nG, nF)
    F2 = F

    F3 = axiom.A3(F, G)
    F4 = MP(F1, F3)
    F5 = axiom.A1(F, nG)

    f6 = syl_1(F5, F4)
    F6 = f6[-1]
    F7 = MP(F2, F6)

    proof = [F1, F2, F3, F4, F5]
    proof.extend(f6)
    proof.append(F7)

    ded1 = build_deduction(proof, F2, G)
    ded2 = build_deduction(proof+ded1, F1, F6)

    proof.extend(ded1)
    proof.extend(ded2)

    return proof

def build_T5(F,G):
    nF = notFormula(F)
    nG = notFormula(G)

    t5 = Node(Node(F, G),Node(nG, nF))
    t5.msg = "T5 for F, G. proof not implemented"

    return [t5]

def build_T6(F, G):
    nG = notFormula(G)
    fg = Node(F, G, _not=True)

    t6 = Node(F,
              Node(nG, fg))

    t6.msg = "T6 for F,G. proof not implemented"

    return [t6]

def Calmar_Theorem(F:Node, values):
    '''
        Calmar's Theorem implementation

    :param F: Propositional calculus formula: Variable or Node
    :return:
    '''

    if type(F) == Variable:
        v = Variable(F.symbol, F._not)
        v.msg = "Calmar's theorem, induction base"

        return [v]

    if F._not:  # F = !G
        G = Node(None, None)
        G.left = F.left     # Copy G, but F = !G
        G.right = F.right

        if F.calculate(values) == 1:
            G.msg = "Calmar's theorem, 1.a) F^(alpha) = G^(alpha) => hypoth |- G^() = F^()"

            return [G]

        else:
            # !f = !!g
            t2 = build_T2(G)
            T2 = t2[-1]

            nng = MP(G, T2)

            res = t2
            res.append(nng)
            return res

    else:   # F = G->H

        res = []

        G = F.left
        H = F.right

        if G.calculate(values) == 0:

            t3 = build_T3(G, H)

            T = t3[-1]
            mp = MP(G, T)

            res = t3
            res.append(mp)

        elif H.calculate(values) == 1:

            # h->(g->h)
            h = H
            hgh = axiom.A1(H,G)

            gh = MP(h, hgh)

            return [hgh, gh]

        else:
            # F = !(G->H)
            # have G, !H. proof !(G->H)

            nH = notFormula(H)

            t6 = build_T6(G, H)
            T6 = t6[-1]

            f1 = MP(G, T6)
            f2 = MP(nH, f1)

            res = t6
            res.extend([f1, f2])

        return res

def Ad_Theorem(F):
    '''

        Adequacy theorem implementation

    :param F: Propositional calculus formula: Variable or Node
    :return: formal proof |- F
    '''

    proof = []

    symbols = list(F.used_symbols())
    symbolsCount = len(symbols)

    N = 1<<symbolsCount

    vector = 0 # why not int for vector?
    n = 0

    while n<len(symbols):
        vector = 0
        while vector<N:
            X_n = symbols[n]
            values = {symbols[k]: 0 if vector&(1<<k) == 0 else 1 for k in range(len(symbols))}
            values_not = values.copy()

            values[X_n] = 1
            values[X_n] = 0

            C1 = Calmar_Theorem(F, values)
            C2 = Calmar_Theorem(F, values_not)
            proof.extend(C1)
            proof.extend(C2)

            deduct = build_deduction(proof, Variable(X_n), F)
            if not deduct is None:
                proof.extend(deduct)

            deduct = build_deduction(proof, Variable(X_n, _not=True), F)

            if not deduct is None:
                proof.extend(deduct)

            if len(C1) == 0 or len(C2) == 0:
                vector+=1
                continue

            t7 = axiom.T7(Variable(X_n), F)
            mp1 = MP(C1[-1], t7)
            mp2 = MP(C2[-1], mp1)

            proof.extend([t7, mp1, mp2])

            vector+=1
        n+=1

    return proof

if __name__ == '__main__': # some tests

    a = Variable('A')
    nA = notFormula(a)
    nna = notFormula(nA)

    F = Node(a, nna)

    proof = Ad_Theorem(F)

    index = 0
    for p in proof:
        if p is None:
            continue
        print(str(index) + '.\t' + str(p) + '\n' + p.msg + '\n\n')
        index+=1

        if p == F:
            break