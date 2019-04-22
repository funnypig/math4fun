

class IncorrectInput(Exception):
    def __str__(self):
        return 'Incorrect formula'


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

class Variable:
    """
        Represents single variable or it's negative value -
            the letter from A to Z, or !A, ... ,!Z
    """
    def __init__(self, symbol, _not = False, msg = ""):
        self.symbol = symbol
        self._not = _not
        self.msg = msg

    def calculate(self, values):
        return lnot(values[self.symbol]) if self._not else values[self.symbol]

    def show(self):
        if self._not:
            print('!',end='')
        print(self.symbol, end='')

    def __str__(self):
        res = ''

        if self._not:
            res = '!'

        res += self.symbol

        return res

    def __eq__(self, other):
        return str(self) == str(other)

    def used_symbols(self):
        return {self.symbol}

class Node:
    """
        Represents formula:
            - Variable -> Variable
            - Variable -> Node
            - Node -> Variable
            - Node -> Node

        if left or right is single symbol it will be represented as Variable
        if there is combination of variables in parentheses it will be Node

        f.e. A->!(B->C)     =>  Variable -> Node
             (B->C)->A      =>  Node -> Variable

        Both Variable and Node has 'calculate' function,
        so it is not problem to calculate child of the tree in spite of its type
    """

    def __init__(self, left, right, _not = False, msg = ''):
        self.left = left
        self.right = right
        self._not = _not
        self.msg = msg

    def calculate(self, values):
        res = implication(self.left.calculate(values), self.right.calculate(values))
        if self._not:
            res = lnot(res)

        return res

    def show(self):
        if self._not:
            print('!',end='')
        print('(', end='')
        self.left.show()
        print('->', end='')
        self.right.show()
        print(')', end='')

    def __str__(self):
        res = ''

        if self._not:
            res = '!'
        res = res + '(' + str(self.left) + ') -> (' + str(self.right) + ')'

        return res

    def __eq__(self, other):
        return str(self) == str(other)

    def used_symbols(self):
        s = str(self)
        _symbols = set()

        for si in s:
            if si in VARS:
                _symbols.add(si)

        return _symbols

def buildFormula(s):
    """
    build the sequence of nodes
    :param s: list of operations
    f.e. A->!B  =>  [A, ->, !B]
    :return: Node
    """

    def get_node():

        nonlocal s

        _not = False
        if s[0] == '!':
            _not = True
            s.pop(0)

        node = None

        if s[0] in VARS:
            symbol = s.pop(0)
            node = Variable(symbol, _not)
            return node
        elif s[0] == '(':
            s.pop(0)
            left = get_node()
            right = None

            if s[0]==')':
                s.pop(0)
                return left
            elif s[0] == '>':
                s.pop(0)
                right = get_node()
            s.pop(0)

            if right is None:
                return left
            else:
                node = Node(left, right, _not)
                return node
        else:
            raise IncorrectInput()


    """
        left -> right
    """
    left = get_node()

    """
        (left) or left
            is possible too
    """
    if len(s) == 0:
        return left

    """
        but implication is required if formula continues
    """
    if s[0] == '>':
        s.pop(0)
    else:
        raise IncorrectInput()

    right = get_node()

    return Node(left, right)



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

