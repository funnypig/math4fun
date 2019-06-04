
import axiom
from axiom import MP
from formula import Variable, Node, notFormula
import formula

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

def build_deduction(hypoth, F, G, proof = []):
    """
        hypoth, F |- G => hypoth |- F->G

        proof = [F1, ..., Fn-1] + [G]
        F = Fn
    """

    if len(proof) == 0 or proof[-1]!=G:
        proof.append(G)

    res = []

    P_index = -1

    for p in proof:
        P_index+=1

        if p==F:
            res.extend(build_TL(F))

        elif axiom.if_Axiom(p) or p in hypoth:

            # A1 for F, G
            F1 = axiom.A1(p,F)
            # MP for F and F1
            F2 = axiom.MP(p, F1)

            res.extend([F1, F2])

        else:
            # smth weird happens here
            _str = p.msg

            if not _str.startswith("MP for"):
                continue

            _str = _str.replace("MP for", "")

            sFr, sFs = _str.split(',')
            Fr = formula.buildFormula(formula.prepareString(sFr))
            Fs = formula.buildFormula(formula.prepareString(sFs))

            # A2 for G, Fr, F
            F1 = axiom.A2(F, Fr, p)

            # MP for F1, G->Fs
            F2 = axiom.MP(Node(F, Fs), F1)

            # MP for G->Fr, F2
            F3 = axiom.MP(Node(F, Fr), F2)

            res.extend( [F1, F2, F3] )

    return res

def syl_1(F, G):
    # F = F->G; G = G->H
    F1 = F.left

    F4 = MP(F1, F)
    F5 = MP(F4, G)

    res = [F, G, F1, F4]
    res.extend(build_deduction([F,G], F1, F5, res))

    return res

def syl_2(F, G):
    # F->(G->H), G |- F->H

    F3 = F.left # A
    F4 = MP(F3, F) # B->C
    F5 = MP(G, F4) # C

    proof = build_deduction([F, G], F3, F5, [F, G, F3, F4, F5]) # A->C

    return proof

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

    f13 = build_deduction([F1, F2, F9], F8, F12, [F8, F9, F10]+f11+[F12])
    F13 = f13[-1]
    f14 = build_deduction([], F9, F13, f13)
    F14 = f14[-1]

    #...
    f15 = syl_1(F14, F7)
    F15 = f15[-1]
    f16 = syl_1(F15, F6)
    F16 = f16[-1]

    proof = [F1, F2] + f14 + [F4] + f5

    f17 = build_deduction([], F1, F16, proof)

    proof = f17

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

    proof = [F1, F2, F3, F4, F5, F6, F7, F8, F9]

    ded1 = build_deduction([F1], F, G, proof)
    proof = ded1
    ded2 = build_deduction([], F1, ded1[-1], proof)
    proof = ded2

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

    proof = [F3, F4, F5]
    proof.extend(f6)

    proof = build_deduction([F1,F], F1, f6[-1], proof)

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

    f2 = build_T2(G)
    F2 = f2[-1]

    F3 = axiom.A3(nG, nF)

    f4 = syl_1(F1, F2) # f->!!g
    F4 = f4[-1]

    f5 = build_T1(F)
    F5 = f5[-1]

    f6 = syl_1(F5, F4) # !!f->!!g
    F6 = f6[-1]

    F7 = MP(F6, F3) # (!!f->!g)->!f

    F8 = axiom.A1(nG, nnF)

    f9 = syl_1(F8, F7)
    F9 = f9[-1]

    proof = f2 + [F3] + f4 + f5 + f6 + [F7, F8] + f9

    proof = build_deduction([F1, nG], F1, F9, proof)

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
    ded = build_deduction([F1, ng], fg, G, [F1, F2])
    F3 = ded[-1]

    F4 = MP(F3, T5)

    proof = [F1, ng, F2] + ded + [F4]

    proof = build_deduction([], F, F4, proof)

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


            hypo = [Variable(k, _not = True if v == 0 else False) for k,v in values.items()]
            deductC1 = build_deduction(hypo, Variable(X_n), F, C1)

            hypo = [Variable(k, _not = True if v == 0 else False) for k,v in values.items()]
            deductC2 = build_deduction(hypo, Variable(X_n, _not=True), F, C2)


            if len(C1) == 0 or len(C2) == 0:
                vector+=1
                continue

            t7 = build_T7(Variable(X_n), F)
            T7 = t7[-1]
            mp1 = MP(C1[-1], T7)
            mp2 = MP(C2[-1], mp1)

            proof.extend(deductC1)
            proof.extend(deductC2)
            proof.extend(t7)
            proof.extend([mp1, mp2])

            curLen = len(proof) #for debug

            vector+=1


        n+=1


    return proof

if __name__ == '__main__':



    f = Variable('F')
    g = Variable('G')

    t4 = build_T4(f,g)
    T4 = t4[-1]
    t5 = build_T5(f,g)
    t6 = build_T6(f,g)
    t7 = build_T7(f,g)
    T7 = t7[-1]

    print('no exception? it is small victory')
