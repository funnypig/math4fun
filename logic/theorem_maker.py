
import axiom
from axiom import MP
from formula import Variable, Node, notFormula

proof = []  # global is not best solution, but as it is

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
        F1 = axiom.A1(G,F)
        # MP for F and F1
        F2 = axiom.MP(G, F1)

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
    res.extend(build_deduction(res, F1, F5))

    return res

def syl_2(F, G):
    # F->(G->H), G |- F->H



    F3 = F.left # A
    F4 = MP(F3, F) # B->C
    F5 = MP(G, F4) # C

    f = build_deduction([F, F3, F4], F3, F5) # A->C

    res = [F3, F4, F5]
    res.extend(f)

    return res

def build_T7(F,G):
    # (F->G)->((!F->G)->G)

    nF = notFormula(F)
    nG = notFormula(G)

    F1 = Node(F,G)
    F1.msg = "t7 hypoth"
    F2 = Node(nF, G)
    F2.msg = "t7 hypoth"

    f3 = build_T5(F,G)
    F3 = f3[-1]
    F4 = axiom.A3(F,G)

    f5 = syl_1(F3, F4)
    F5 = f5[-1]

    F6 = MP(F1, F5)

    f7 = build_T4(nG, F)
    F7 = f7[-1]

    # (!F->G)->(!F->!!G)
    F8 = nF
    F9 = Node(nF, G)
    F10 = MP(F8, F9)
    f11 = build_T2(G)
    F11 = f11[-1]

    F12 = MP(F10, F11)

    proof = [F1, F2] + f3 + [F4] + f5 + [F6] + f7 + [F8, F9, F10] + f11 + [F12]

    f13 = build_deduction(proof, F8, F12)
    F13 = f13[-1]
    f14 = build_deduction(proof, F9, F13)
    F14 = f14[-1]

    #...
    f15 = syl_1(F14, F7)
    F15 = f15[-1]
    f16 = syl_1(F15, F6)
    F16 = f16[-1]

    f17 = build_deduction(proof, F1, F16)

    proof += f13 + f14 + f15 + f16 + f17

    return proof

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

    f2 = build_T1(nF) # build th. 1
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
    nG = notFormula(G)

    F1 = notFormula(F)
    F2 = F

    F3 = axiom.A1(F2, nG)
    F4 = MP(F2, F3)

    F5 = axiom.A1(F1, nG)
    F6 = MP(F1, F5)
    F7 = axiom.A3(F,G)
    F8 = MP(F6, F7)
    F9 = MP(F4, F8)

    hypoth = [F1, F2, F3, F4, F5, F6, F7, F8, F9]

    ded1 = build_deduction(hypoth, F, G)
    ded2 = build_deduction(hypoth+ded1, F1, ded1[-1])

    proof = [F3, F4, F5, F6, F7]
    proof.extend(ded1)
    proof.extend(ded2)

    proof.extend([F8, F9])

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

    ded1 = build_deduction(proof, F2, G)
    ded2 = build_deduction(proof+ded1, F1, F6)


    proof.append(F7)
    proof.extend(ded1)
    proof.extend(ded2)

    return proof

def build_T5(F,G):
    """
        (F->G)->(!G->!F)
    """

    nF = notFormula(F)
    nG = notFormula(G)

    nnF = notFormula(nF)
    nnG = notFormula(nG)

    F1 = Node(F,G)
    F2 = nG

    F3 = axiom.A3(nG, nF) # (!!F->!!G)->((!!F->!G)->!F)
    F4 = axiom.A1(nG, nnF) # !G->(!!F->!G) => MP: !!F->!G
    F45 = MP(nG, F4)

    f5 = build_T2(G)
    F5 = f5[-1]
    f6 = build_T1(F)
    F6 = f6[-1]

    f7 = syl_1(F1, F5)
    F7 = f7[-1]

    f8 = syl_1(F6, F7)
    F8 = f8[-1]

    F9 = MP(F8, F3)
    F10 = MP(F45, F9)

    proof = [F1, F2, F3, F4, F45]
    proof.extend(f5)
    proof.extend(f6)
    proof.extend(f7)
    proof.extend(f8)

    proof.extend([F9, F10])
    proof.extend(build_deduction(proof[:-2], F2, F10))
    proof.extend(build_deduction(proof[:-2], F1, proof[-1]))


    return proof

def build_T6(F, G):
    fg = Node(F,G)
    fg.msg = "hypoth t6"

    t5 = build_T5(fg, G)
    T5 = t5[-1]


    ng = notFormula(G)
    ng.msg = "hypoth t6"
    F1 = F
    F1.msg = "hypoth t6"
    # we need (F->G)->G
    F2 = MP(F1, fg)
    ded = build_deduction([F,fg], fg, G)
    F3 = ded[-1]

    F4 = MP(F3, T5)
    F5 = MP(ng, F4)

    proof = [fg, ng, F1]
    proof.extend(t5)
    proof.append(F2)
    proof.extend(ded)
    proof.extend([F4,F5])

    return proof

def Calmar_Theorem(F, values):
    '''
        Calmar's Theorem implementation

    :param F: Propositional calculus formula: Variable or Node
    :return:
    '''

    if type(F) == Variable:
        v = Variable(F.symbol, _not=True if values[F.symbol] == 1 else 0)

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

            nG = notFormula(G)
            t3 = build_T3(G, H)

            T = t3[-1]
            mp = MP(nG, T)

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

    global proof

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

            # clean
            while None in proof:
                proof.remove(None)

            hypo = [Variable(k, _not = True if v == 0 else False) for k,v in values.items()]
            deduct = build_deduction(hypo, Variable(X_n), F)
            if not deduct is None:
                proof.extend(deduct)

            hypo = [Variable(k, _not = True if v == 0 else False) for k,v in values.items()]
            deduct = build_deduction(hypo, Variable(X_n, _not=True), F)

            if not deduct is None:
                proof.extend(deduct)

            if len(C1) == 0 or len(C2) == 0:
                vector+=1
                continue

            t7 = build_T7(Variable(X_n), F)
            T7 = t7[-1]
            mp1 = MP(C1[-1], T7)
            mp2 = MP(C2[-1], mp1)

            proof.extend(t7)
            proof.extend([mp1, mp2])

            vector+=1


        n+=1


    # clean doubles

    i1 = 0
    while i1<len(proof):
        i2 = i1+1
        while i2<len(proof):
            if proof[i2] == proof[i1]:
                proof.pop(i2)
            else:
                i2+=1
        i1+=1

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