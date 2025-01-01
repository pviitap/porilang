"""
porilang

"""


from functools import reduce
from enum import Enum
from pprint import pprint

TYPE = Enum('TYPE', [('NUMBER', 1), ('SYMBOL', 2), ('OPERATOR', 3)])
SYMBOL = Enum('SYMBOL', [('san', 1), ('o', 2)])
OPERATOR = Enum('OPERATOR', [('+', 1), ('-', 2), ('*', 3), ('/', 4)])

class Token:
    value: int | SYMBOL | OPERATOR
    type: TYPE
    def __init__(self, value, type):
        self.value = value
        self.type = type
    def __repr__(self):
        return "value: " + str(self.value) + ", type: " + str(self.type)
class State:
    stack: list
    identifiers: dict
    def __init__(self, stack, identifiers):
        self.identifiers = identifiers
        self.stack = stack

def push_to_stack(item, stack: list) -> list:
    stack.append(item)
    return stack

def pop_from_stack(stack) -> list:
    return stack.pop()


def tokenize(code : str) -> list:
    """
    tokenize the code

    """

    list_of_words = [ line.strip().split() for line in
             code.strip().split("\n")
            if line != "" and not line.startswith("#") ]
    words = reduce(lambda x, y: x + ['\n'] +  y, list_of_words) + ['\n']
    length = len(words)

    tokens : list[Token] = []
    for i in range(0,length):
        curtoken = words[i]
        if curtoken.isnumeric():
            tokens.append(Token(int(curtoken), TYPE.NUMBER))
        elif curtoken in SYMBOL._member_names_:
            tokens.append(Token( SYMBOL[curtoken], TYPE.SYMBOL))
        elif curtoken in OPERATOR._member_names_:
            tokens.append(Token( OPERATOR[curtoken], TYPE.OPERATOR))
        else:
            tokens.append(Token( curtoken, None))
            #raise ValueError('Could not parse ' + curtoken)
    return tokens

def parse_expression(tokens: list[Token], state: State) -> tuple[Token, list[Token]]:
    """
    <expression> = number | identifier
    """
    curtoken, tokens_left = next_token(tokens)
    if curtoken.type == TYPE.NUMBER:
        push_to_stack(curtoken.value, state.stack)
    else: #todo check identifier type?
        push_to_stack(state.identifiers[curtoken.value], state.stack)

    #raise ValueError("Expected: expression but is " + str(curtoken))

    return (curtoken, tokens_left)

def parse_print_statement(tokens: list[Token], state: State) -> tuple[Token, list[Token]]:
    """
    <print_statement> = "san" <expression>
    """
    curtoken, tokens_left = next_token(tokens)
    if curtoken.value != SYMBOL.san:
        raise ValueError("Expected: san")

    curtoken, tokens_left = parse_expression(tokens_left, state)
    print("se o " + str(pop_from_stack(state.stack)))
    return (curtoken, tokens_left)

def parse_assignment(tokens: list[Token], state: State) -> tuple[Token, list[Token]]:
    """
    <assignment> = identifier "o" <expression>
    """

    curtoken, tokens_left = next_token(tokens)
    identifier = curtoken.value

    curtoken, tokens_left = next_token(tokens_left)
    if curtoken.value != SYMBOL.o:
        raise ValueError("Expected: o")

    curtoken, tokens_left = parse_expression(tokens_left, state)

    state.identifiers[identifier] = pop_from_stack(state.stack)
    
    return (curtoken, tokens_left)

def next_token(tokens: list[Token]) -> tuple[Token, list[Token]]:
    curtoken = tokens[0]
    tokens_left = tokens[1:]
    return (curtoken, tokens_left)

def parse_statement(tokens: list[Token], state: State) -> tuple[Token, list[Token]]:

    if tokens[0].value == SYMBOL.san:
        curtoken, tokens_left = parse_print_statement(tokens, state)
    else:
        curtoken, tokens_left = parse_assignment(tokens, state)
    
    curtoken, tokens_left = next_token(tokens_left)
    if curtoken.value != '\n':
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

    """
    with open('test.pori','r',encoding='UTF-8') as f:
        tokens = tokenize(f.read())

    tokens = tokenize('''a o 3
                      san 1
                      san 2
                      san a
                      san 4
                      ''')
    """

    tokens = tokenize('''a o 3
                      b o 1
                      san b
                      san a
                      ''')

    pprint(parse_program(tokens))
    print("done")
