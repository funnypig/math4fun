

class IncorrectInput(Exception):
    def __str__(self):
        return 'Incorrect formula'

GLOBAL_ID = 0

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
        global GLOBAL_ID
        self.id = GLOBAL_ID
        GLOBAL_ID+=1

        self.symbol = symbol
        self._not = _not
        self.msg = msg

    def calculate(self, values):
        return lnot(values[self.symbol]) if self._not else values[self.symbol]

    def show(self):
        if self._not:
            print('!({})'.format(self.symbol),end='')
        else:
            print(self.symbol, end='')

    def __str__(self):
        res = ''

        if self._not:
            res = '!({})'.format(self.symbol)
        else:
            res = self.symbol

        return res

    def __eq__(self, other):
        return str(self) == str(other)

    def used_symbols(self):
        return {self.symbol}


"""
    IMPORTANT CLAIM:
        'single' parameter introduced below to allow use double not to formula
        f.e. it was unable to use !!(A->B) earlier
        now it will be 
            Node0: _not = true, single = Node1
            Node1: _not = true, single = Node
            Node: left = A, right = B

"""

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

    def __init__(self, left, right, _not = False, msg = '', single = None):
        global GLOBAL_ID
        self.id = GLOBAL_ID
        GLOBAL_ID += 1

        if not single is None:
            self.single = single
            self.msg = msg
            self._not = _not
            self.msg = msg
            return

        self.left = left
        self.right = right
        self._not = _not
        self.msg = msg

        self.single = None

    def calculate(self, values):

        if not self.single is None:
            res = self.single.calculate(values)
            return lnot(res) if self._not else res

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

        if not self.single is None:
            if self._not:
                res = '!('+str(self.single)+')'
            else:
                res = str(self.single)

            return res

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

def notFormula(tree):
    nt = Node(None, None, _not=True, msg="NOT added to: "+tree.msg, single=tree)
    return nt

def buildFormula(s):
    """
    build the sequence of nodes
    :param s: list of operations
    f.e. A->!B  =>  [A, ->, !B]
    :return: Node
    """


    if type(s) == str:
        s = list(s)

    def get_node():

        nonlocal s

        _not = False
        if s[0] == '!':
            _not = True

            s.pop(0)

            node = get_node()
            node = notFormula(node)

            return node

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

'''
if __name__ == '__main__':


    s = "!!F->F"
    s = "F->!!F"
    s = prepareString(s)
    f = buildFormula(s)

    print(f)
    print(f.calculate({"F":1}))
    print(f.calculate({"F":0}))

    exit()

    f = buildFormula(prepareString('!A->(B->A)'))


    f0 = buildFormula(prepareString('A->B'))
    f1 = notFormula(f0)
    f2 = notFormula(f1)



    F = buildFormula(prepareString("((A->B)->A)->A"))

    print(f0, 'Calc:',f0.calculate({'A':1, 'B':0}))
    print(f1, 'Calc:',f1.calculate({'A':1, 'B':0}))
    print(f2, 'Calc:',f2.calculate({'A':1, 'B':0}))
    print(F)
    print()

    a = Variable('A')
    na = notFormula(a)
    nna = notFormula(na)

    print(a, 'Calc:',a.calculate({'A':1}))
    print(na, 'Calc:',na.calculate({'A':1}))
    print(nna, 'Calc:',nna.calculate({'A':1}))
'''