import pytest
from porilang import tokenize, Token, TYPE

def test_tokenizer():

    code = 'a 1 2'
    tokens = tokenize(code)

    assert  tokens[0].value == 'a'
    assert  tokens[0].type == None


    assert  tokens[1].value == 1
    assert  tokens[1].type == TYPE.NUMBER
