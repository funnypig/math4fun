
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

VARS = [chr(i) for i in range(ord('A'), ord('Z')+1)] # variable symbols

def implication(a, b):
    """
    calculates logical implication by the rule:

    a | b | a->b
    ------------
    0 | 0 |  1
    0 | 1 |  1
    1 | 0 |  0
    1 | 1 |  1

    :param a: 0 or 1
    :param b: 0 or 1
    :return: the result of calculation
    """

    if a == 1 and b == 0:
        return 0

    return 1

def lnot(a):
    """
    calculates logical not by the rule:

    a | !a
    ------
    0 | 1
    1 | 0

    :param a: 0 or 1
    :return: the result of calculation
    """

    return 0 if a == 1 else 1

class Node:
    """
        Represents the variable symbol of the node.
        If the node is formula, I replace it with variable and represent as Node.

        F.e.
        Let F = A -> (B -> !C)

        F is node.
        A is node.
        B is node.
        !C is node.

        Let's calculate (B -> !C), then replace it with D = (B -> !C), now we can set D as Node.
    """
    def __init__(self, symbol = None, _not = False, operation = None, this = None, next = None):
        self.symbol = symbol
        self._not = _not
        self.operation = operation
        self.this = this
        self.next = next

    def calculate(self, values):
        a = values[self.symbol] if not self.symbol is None else self.this.calculate(values)

        if self._not:
            a = lnot(a)

        if self.operation is None:
            return a
        else:
            return self.operation(a, self.next.calculate(values))

    def show(self):

        print(('!' if self._not else ''), end='')

        if not self.symbol is None:
            print(self.symbol, end='')

        if not self.this is None:
            print('(',end='')
            self.this.show()
            print(')',end='')

        if not self.next is None:
            print('->',end='')
            if not self.next is None:
                self.next.show()


def buildFormula(s):
    """
    build the sequence of nodes
    :param s: list of operations
    f.e. A->!B  =>  [A, ->, !B]
    :return: Node
    """

    if s is None or len(s) == 0:
        return None
    if s[0] == ')':
        s.pop(0)
        return None

    node = None
    symbol = ''
    _not = False
    operation = None

    if s[0] == '!':
        _not = True
        s.pop(0)

    if s[0] == '(':
        """
            ( ... ) ... => ... ) ...
            make formula with ...
            => ) ... => ...
        """
        s.pop(0)
        node = buildFormula(s)
        if len(s) != 0 and s[0] == ')': s.pop(0)
    else:
        symbol = s.pop(0)

    # pop operation
    if len(s)!=0 and s[0] == '>':
        operation = implication
        s.pop(0)

    nextNode = buildFormula(s)

    if node is None:
        node = Node(symbol=symbol, _not = _not, operation = operation, next = nextNode)
    else:
        node = Node(this = node, _not = _not, operation = operation, next = nextNode)
    return node

def prepareString(s:str):
    """
        Prepare string for parsing:
            - remove spaces and tabs
            - capitalize (user may make typo)
            - strip
            - replace '->' on '>' to make parsing easier

    :param s: input string
    :return: prepared string
    """

    s = s.upper().strip().replace('\t','').replace(' ','').replace('->','>')

    return s


def bruteforce(tree, symbols):
    index = 0
    for i in range(2**(len(symbols)+1)):
        values = {
            symbols[k] : 0 if (index & (1<<k))==0 else 1 for k in range(len(symbols))
        }
        c = tree.calculate(values)

        if c == 0:
            return False, values

        index+=1

    return True, None

def analyze(tree):
    # TODO
    pass

def test():
    tests = [
        "A->B", "\ta ->           b    ",
        "(A->B)->!(!A->!B)",
        "!A->!B",
        "!(A->!B)",
        "!A->(A->A)",
        "!A->!(!B->(!C->A))"
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
            print('Tautology')
        else:
            print('NOT tautology')
            print('Crashes on:', res)

        print()

def userInput():
    print('Input formula:')
    s = input()
    s = prepareString(s)
    s =  list(s)

    symbols = set()
    for _s in s:
        if _s in VARS:
            symbols.add(_s)

    tree = buildFormula(s)

    print('Symbols:',symbols)

    ifTau, res = bruteforce(tree, list(symbols))
    if ifTau:
        print('Tautology')
    else:
        print('NOT tautology')
        print('Crashes on:',res)

if __name__ == '__main__':
    test()