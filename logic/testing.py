from formula import *
from tautology_checker import *

def test():
    tests = [
        "A->B", "\ta ->           b    ",
        "(A->B)->!(!A->!B)",
        "!A->!B",
        "!(A->!B)",
        "!A->(A->A)",
        "!A->!(!B->(!C->A))",
        "(a->(b->(c->!a)))->a",
        "(!a->(b->(c->!a)))->a",
        "!(a->(b->(c->!a)))->a"
    ]

    for t in tests:
        print("Input formula:",t)
        s = prepareString(t)
        print("Prepared formula:", s)

        symbols = set()
        for _s in s:
            if _s in VARS:
                symbols.add(_s)

        s = list(s)
        tree = buildFormula(s)

        print('Symbols:', symbols)

        ifTau, res = bruteforce(tree, list(symbols))
        if ifTau:
            print('Bruteforce: Tautology')
        else:
            print('Bruteforce: NOT tautology\tCrashes on:', res)

        ifTau, msg = analyze(tree, list(symbols))
        if ifTau:
            print("Analyze: Tautologu")
        else:
            print("Analyze: NOT tautologu")
            print('Message:', msg)

        print()

def newinput():
    s = input()

    if s == 'exit':
        return False

    s = prepareString(s)
    s =  list(s)

    symbols = set()
    for _s in s:
        if _s in VARS:
            symbols.add(_s)

    tree = buildFormula(s)
    print("Show formula:")
    tree.show()
    print()

    #print('Symbols:',symbols)

    ifTau, res = bruteforce(tree, list(symbols))
    if ifTau:
        print('Bruteforce: Tautology')
    else:
        print('Bruteforce: NOT tautology\tCrashes on:',res)

    ifTau, msg = analyze(tree, list(symbols))
    if ifTau:
        print("Analyze: Tautology")
    else:
        print("Analyze: NOT tautology")
        print('Message:',msg)

    print()

    return True

def userInput():
    print('Input formula or "exit":')
    while newinput():
        print('Input formula or "exit":')

def test2():
    tests = [
        "F->(G->F)",
        "(!G -> !F) -> ( (!G -> F) -> G ) ",
        "(F -> (G -> H)) -> ( (F -> G) -> (F -> H) )"
    ]

    for t in tests:
        s = prepareString(t)

        symbols = set()
        for _s in s:
            if _s in VARS:
                symbols.add(_s)
        symbols = list(symbols)

        s = list(s)
        tree = buildFormula(s)

        print("Tree:", str(tree))

        ifTau, msg = bruteforce(tree, symbols)

        print(ifTau)
        print(msg)

        print()


if __name__ == '__main__':
    test2()
    #test()
    userInput()