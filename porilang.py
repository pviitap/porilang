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
        return str(self.tvalue) + " (" + str(self.ttype) + ")"

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

def parse_expression(tokens: list[Token], stack: list) -> tuple:
    curtoken = tokens[0]
    if curtoken.ttype != TType.NUMBER:
        raise ValueError("Expected: expression")

    push(curtoken.tvalue, stack)
    tokens_left = tokens[1:]
    return (tokens_left, stack)

def parse_print_statement(tokens: list[Token], stack: list):
    curtoken = tokens[0]
    if curtoken.tvalue != TSYMBOL.san:
        raise ValueError("Expected: san")

    tokens_left = tokens[1:]
    tokens_left, stack = parse_expression(tokens_left, stack)

    print("se o " + str(pop(stack)))

    return tokens_left

def parse_statement(tokens: list[Token], stack: list):
    tokens_left = parse_print_statement(tokens, stack)

    curtoken = tokens_left[0]
    if curtoken.tvalue != '\n':
        raise ValueError("Expected: end of line")

    tokens_left = tokens_left[1:]

    return tokens_left

def parse_program(tokens: list[Token]):
    """
    parse the code

    <program> = <statement> [ <statement> ... ]
    <statement> = <print_statement> "\n"
    <print_statement> = "san" <expression>
    <expression> = number
    """

    stack : list = []

    if len(tokens)>1:
        while len(tokens)>0:
            tokens = parse_statement(tokens, stack)
        return True
    else:
        return False

if __name__ == '__main__':

    with open('test.pori','r',encoding='UTF-8') as f:
        tokens = tokenize(f.read())

    tokens = tokenize('''san 52
                      san 10 ''')

    pprint(parse_program(tokens))
    print("done")
