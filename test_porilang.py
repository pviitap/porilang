import pytest
from porilang import Porilang, TYPE, SYMBOL

def test_tokenizer():

    code = '''täsä o 1 + 2'''

    porilang = Porilang()
    tokens = list(porilang.tokenize(code))

    assert  tokens[0].value == 'täsä'
    assert  tokens[0].type == TYPE.IDENTIFIER

    assert  tokens[1].value == SYMBOL.o
    assert  tokens[1].type == TYPE.SYMBOL

    assert  tokens[2].value == 1
    assert  tokens[2].type == TYPE.NUMBER

def test_assign():

    code = '''täsä o 5
    tosa o 3
    '''

    porilang = Porilang()
    porilang.run(code)

    assert  porilang.identifiers['täsä'] == 5
    assert  porilang.identifiers['tosa'] == 3

def test_addition():

    code = '''täsä o 1 + 2'''

    porilang = Porilang()
    porilang.run(code)

    assert  porilang.identifiers['täsä'] == 3
