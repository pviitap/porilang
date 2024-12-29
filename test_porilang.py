import pytest
from porilang import tokenize, Token, TType

def test_tokenizer():

    code = 'a 1 2'
    tokens = tokenize(code)

    assert  tokens[0].tvalue == 'a'
    assert  tokens[0].ttype == None


    assert  tokens[1].tvalue == 1
    assert  tokens[1].ttype == TType.NUMBER
