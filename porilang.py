"""
porilang

"""

from dataclasses import dataclass
from functools import reduce
from enum import Enum
from pprint import pprint

TYPE = Enum('TYPE', ['NUMBER', 'SYMBOL', 'OPERATOR', 'IDENTIFIER'])
SYMBOL = Enum('SYMBOL', ['san', 'o'])
OPERATOR = Enum('OPERATOR', [('+', 'add'), ('-', 'sub'), ('*', 'mult'), ('/', 'div')])


@dataclass
class Token:
    value: int | str | SYMBOL | OPERATOR
    type: TYPE

@dataclass
class State:
    stack: list
    identifiers: dict

def push_to_stack(item, stack: list) -> list:
    stack.append(item)
    return stack

def pop_from_stack(stack) -> int:
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
            tokens.append(Token(int(curtoken), TYPE['NUMBER']))
        elif curtoken in SYMBOL._member_names_:
            tokens.append(Token( SYMBOL[curtoken], TYPE['SYMBOL']))
        elif curtoken in OPERATOR._member_names_:
            tokens.append(Token( OPERATOR[curtoken], TYPE['OPERATOR']))
        else:
            tokens.append(Token( curtoken, TYPE['IDENTIFIER']))
            #raise ValueError('Could not parse ' + curtoken)
    return tokens


def parse_expression(tokens: list[Token], state: State) -> tuple[Token, list[Token]]:
    """
    <expression> = <value> [ <operator> <expression> ]
    <operator> = "+" | "-" | "*" | "/"
    <value> = number | identifier
    """

    curtoken, tokens_left = next_token(tokens)
    if curtoken.type == TYPE['NUMBER']:
        push_to_stack(curtoken.value, state.stack)
    elif curtoken.type is TYPE['IDENTIFIER']:
        push_to_stack(state.identifiers[curtoken.value], state.stack)
    else:
        raise ValueError("Expected: <value> [ <operator> <expression> ] but got " + str(curtoken))

    if tokens_left[0].type == TYPE['OPERATOR']:
        curtoken, tokens_left = next_token(tokens_left)
        operator = curtoken.value
        curtoken, tokens_left = parse_expression(tokens_left, state)
        if operator == OPERATOR['+']:
            result = pop_from_stack(state.stack) + pop_from_stack(state.stack)
            push_to_stack(result, state.stack)
        elif operator == OPERATOR['-']:
            v1 = pop_from_stack(state.stack)
            v2 = pop_from_stack(state.stack)
            result = v2 - v1
            push_to_stack(result, state.stack)
        else:
            raise ValueError('unknown operator')

    return curtoken, tokens_left

def parse_print_statement(tokens: list[Token], state: State) -> tuple[Token, list[Token]]:
    """
    <print_statement> = "san" <expression>
    """
    curtoken, tokens_left = next_token(tokens)
    if curtoken.value != SYMBOL['san']:
        raise ValueError("Expected: san")

    curtoken, tokens_left = parse_expression(tokens_left, state)
    print("se o " + str(pop_from_stack(state.stack)))
    return curtoken, tokens_left

def parse_assignment(tokens: list[Token], state: State) -> tuple[Token, list[Token]]:
    """
    <assignment> = identifier "o" <expression>
    """

    curtoken, tokens_left = next_token(tokens)
    identifier = curtoken.value

    curtoken, tokens_left = next_token(tokens_left)
    if curtoken.value != SYMBOL['o']:
        raise ValueError("Expected: o")
    curtoken, tokens_left = parse_expression(tokens_left, state)
    state.identifiers[identifier] = pop_from_stack(state.stack)
    return curtoken, tokens_left

def next_token(tokens: list[Token]) -> tuple[Token, list[Token]]:
    curtoken = tokens[0]
    tokens_left = tokens[1:]
    return curtoken, tokens_left

def parse_statement(tokens: list[Token], state: State) -> tuple[Token, list[Token]]:
    """
    <statement> = (<print_statement> | <assignment>) "\n"
    """

    if tokens[0].value == SYMBOL['san']:
        curtoken, tokens_left = parse_print_statement(tokens, state)
    elif tokens[1].value == SYMBOL['o']:
        curtoken, tokens_left = parse_assignment(tokens, state)
    else:
        raise ValueError("Could not parse assignment")

    curtoken, tokens_left = next_token(tokens_left)
    if curtoken.value != '\n':
        raise ValueError("Expected: end of line")
    return curtoken, tokens_left

def parse_program(tokens: list[Token]) -> bool:
    """
    <program> = <statement> [ <statement> ... ]
    """

    state: State = State([], {})

    print("eläk sääki viä")

    if len(tokens)>1:
        while len(tokens)>0:
            curtoken, tokens = parse_statement(tokens, state)
        print("ei mittää")
        return True

    print("täh?")
    return False

if __name__ == '__main__':

    #parse_program(tokenize('''
    #    a o 5 - 2
    #    san a
    #'''))

    with open('test.pori','r',encoding='UTF-8') as f:
        data = f.read()
    parse_program(tokenize(data))
