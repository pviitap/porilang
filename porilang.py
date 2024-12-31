"""
porilang


a o 4 + 5
san a

"""
from functools import reduce
from enum import Enum
from pprint import pprint

TType = Enum('TType', [('NUMBER', 1), ('SYMBOL', 2), ('OP', 3)])
TSYMBOL = Enum('TSYMBOL', [('san', 1), ('o', 2)])
TOP = Enum('TOP', [('+', 1), ('-', 2), ('*', 3), ('/', 4)])

class Token:
    tvalue: int | TSYMBOL | TOP
    ttype: TType
    def __init__(self, tvalue, ttype):
        self.tvalue = tvalue
        self.ttype = ttype
    def __repr__(self):
        return "value: " + str(self.tvalue) + ", type: " + str(self.ttype)

class State:
    stack: list
    identifiers: dict
    def __init__(self, stack, identifiers):
        self.identifiers = identifiers
        self.stack = stack


def tokenize(code : str) -> list:
    """
    tokenize the code
    """

    list_of_words = [ line.strip().split() for line in
             code.strip().split("\n")
            if line != "" and not line.startswith("#") ]
    #tokens = reduce(lambda x, y: x + ['\n'] + y, list_of_words)
    words = reduce(lambda x, y: x + ['\n'] +  y, list_of_words) + ['\n']
    length = len(words)

    tokens : list[Token] = []
    for i in range(0,length):
        curtoken = words[i]
        if curtoken.isnumeric():
            tokens.append(Token(int(curtoken), TType.NUMBER))
        elif curtoken in TSYMBOL._member_names_:
            tokens.append(Token( TSYMBOL[curtoken], TType.SYMBOL))
        elif curtoken in TOP._member_names_:
            tokens.append(Token( TOP[curtoken], TType.OP))
        else:
            tokens.append(Token( curtoken, None))
            #raise ValueError('Could not parse ' + curtoken)
    return tokens

def push(item, stack: list) -> list:
    stack.append(item)
    return stack

def pop(stack) -> list:
    return stack.pop()

def parse_expression(tokens: list[Token], state: State) -> tuple[Token, list[Token]]:
    """
    <expression> = number | identifier
    """
    curtoken, tokens_left = next_token(tokens)
    if curtoken.ttype == TType.NUMBER:
        push(curtoken.tvalue, state.stack)
    else: #todo check identifier type?
        push(state.identifiers[curtoken.tvalue], state.stack)

    #raise ValueError("Expected: expression but is " + str(curtoken))

    return (curtoken, tokens_left)

def parse_print_statement(tokens: list[Token], state: State) -> tuple[Token, list[Token]]:
    """
    <print_statement> = "san" <expression>
    """
    curtoken, tokens_left = next_token(tokens)
    if curtoken.tvalue != TSYMBOL.san:
        raise ValueError("Expected: san")

    curtoken, tokens_left = parse_expression(tokens_left, state)
    print("se o " + str(pop(state.stack)))
    return (curtoken, tokens_left)

def parse_assignment(tokens: list[Token], state: State) -> tuple[Token, list[Token]]:
    """
    <assignment> = identifier "o" <expression>
    """

    curtoken, tokens_left = next_token(tokens)
    identifier = curtoken.tvalue

    curtoken, tokens_left = next_token(tokens_left)
    if curtoken.tvalue != TSYMBOL.o:
        raise ValueError("Expected: o")

    curtoken, tokens_left = parse_expression(tokens_left, state)

    state.identifiers[identifier] = state.stack.pop()
    
    return (curtoken, tokens_left)

def next_token(tokens: list[Token]) -> tuple[Token, list[Token]]:
    curtoken = tokens[0]
    tokens_left = tokens[1:]
    return (curtoken, tokens_left)

def parse_statement(tokens: list[Token], state: State) -> tuple[Token, list[Token]]:

    if tokens[0].tvalue == TSYMBOL.san:
        curtoken, tokens_left = parse_print_statement(tokens, state)
    else:
        curtoken, tokens_left = parse_assignment(tokens, state)
    
    curtoken, tokens_left = next_token(tokens_left)
    if curtoken.tvalue != '\n':
        raise ValueError("Expected: end of line")
    return curtoken, tokens_left

def parse_program(tokens: list[Token]):
    """
    parse the code

    <program> = <statement> [ <statement> ... ]
    <statement> = (<print_statement> | <assignment>) "\n"
    <print_statement> = "print" <expression>
    <assignment> = identifier "=" <expression>
    <expression> = number | identifier
    """

    state: State = State([], {})

    if len(tokens)>1:
        while len(tokens)>0:
            curtoken, tokens = parse_statement(tokens, state)
        return True
    else:
        return False

if __name__ == '__main__':

    with open('test.pori','r',encoding='UTF-8') as f:
        tokens = tokenize(f.read())

    tokens = tokenize('''a o 3
                      san 1
                      san 2
                      san a
                      san 4
                      ''')

    pprint(parse_program(tokens))
    print("done")
