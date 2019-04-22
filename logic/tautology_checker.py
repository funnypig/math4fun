from formula import Variable, Node


def bruteforce(tree, symbols):
    index = 0
    for i in range(2**len(symbols)):
        values = {
            symbols[k] : 0 if (index & (1<<k))==0 else 1 for k in range(len(symbols))
        }

        c = tree.calculate(values)

        if c == 0:
            return False, values

        index+=1

    return True, None

def analyze(tree, symbols):     # TODO: problem with ! before node. does not work correctly
    CONTRADICTION = False

    defined_symbols = {s:-1 for s in symbols}

    """
        Let Formula is NOT tautology
    
        Node -> Node    <=  1->0 to find values which will satisfy Formula(values) = 0
        if Node is Variable then put it's symbols value to 1 else 
            calculate formula inside the node to be 1
        
        f.e.    a->(b->c)
        a = 1                       | => we have defined all values, 
                                    |   and calculation will give 0,
        b->c = 0 => b = 1, c = 0    |   so it's not tautology
        
        f.e.    a->(b->a)   
        a = 1                       |   => CONTRADICTION => TAUTOLOGY
        b->!a = 0   => b = 1, a = 0 |   
    """

    # it's just like A or !A
    if type(tree) == Variable:
        return bruteforce(tree, symbols)[0]


    def define_symbols(node, expected_value):
        nonlocal defined_symbols, CONTRADICTION

        if node is None: return

        if type(node) == Variable:
            symbol = node.symbol
            if node.calculate({symbol:1}) == expected_value:
                if defined_symbols[symbol] == -1:
                    defined_symbols[symbol] = 1

                elif defined_symbols[symbol] != 1:
                    CONTRADICTION = True
                    return

            else:
                if defined_symbols[symbol] == -1:
                    defined_symbols[symbol] = 0

                elif defined_symbols[symbol] != 0:
                    CONTRADICTION = False
                    return

        else:
            if not node._not:
                define_symbols(node.left, 1)
                define_symbols(node.right, 0)

    if not tree._not:
        define_symbols(tree.left, 1)
        define_symbols(tree.right, 0)




    print(defined_symbols)

    if CONTRADICTION:
        return True, 'Contradiction'


    # BRUTE FORCE WITH SYMBOLS THAT ARE NOT DEFINED

    not_defined = []
    static_values = {}

    for sym, val in defined_symbols.items():
        if val == -1:
            not_defined.append(sym)
        else:
            static_values[sym] = val

    # IF ALL DEFINED, WE HAVE JUST TO CALCULATE
    if len(not_defined) == 0:
        if tree.calculate(static_values) == 0:
            return False, str(static_values)
        else:
            return True, ""

    # BRUTE FORCE BY SOME SYMBOLS

    index = 0

    for i in range(2**len(not_defined)):
        local_symbols = static_values.copy()

        for k in range(len(not_defined)):
            if (index & (1 << k)) == 0:
                local_symbols[not_defined[k]] = 0
            else:
                local_symbols[not_defined[k]] = 1

        c = tree.calculate(local_symbols)

        if c == 0:
            return False, 'Crashed on: '+str(local_symbols)

    return True, ''