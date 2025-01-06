import pytest
from porilang import tokenize, parse_program, Token, State, TYPE

def test_tokenizer():

    code = 'a 1 2'
    tokens = tokenize(code)

    assert  tokens[0].value == 'a'
    assert  tokens[0].type == TYPE.IDENTIFIER

    assert  tokens[1].value == 1
    assert  tokens[1].type == TYPE.NUMBER

def test_assign():

    code = '''a o 5
    b o 3
    '''

    state: State = State([], {})
    state = parse_program(tokenize(code), state)

    assert  state.identifiers['a'] == 5
    assert  state.identifiers['b'] == 3


def test_addition():

    code = 'a o 1 + 2'

    state: State = State([], {})
    state = parse_program(tokenize(code), state)

    assert  state.identifiers['a'] == 3

