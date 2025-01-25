"""
porilang

"""

from dataclasses import dataclass
from functools import reduce
from enum import Enum
from pprint import pprint
from typing import Iterator

TYPE = Enum('TYPE', ['NUMBER', 'SYMBOL', 'OPERATOR', 'IDENTIFIER'])
SYMBOL = Enum('SYMBOL', ['san', 'o', 'määrittel', 'loppu', 'tees'])
OPERATOR = Enum('OPERATOR', [('+', 'add'), ('-', 'sub'), ('*', 'mult'), ('/', 'div')])


@dataclass
class Token:
    value: int | str | SYMBOL | OPERATOR
    type: TYPE

class Porilang:
    code: str
    curtoken: Token
    tokens: Iterator[Token]
    stack: list
    identifiers: dict
    line_nr: int

    def __init__(self):
        self.line_nr = 0
        self.stack = []
        self.identifiers = {}

    def next_token(self) -> Token:
        self.curtoken = next(self.tokens)
        return self.curtoken

    def push_to_stack(self, item):
        self.stack.append(item)
    def pop_from_stack(self) -> int:
        return self.stack.pop()

    def tokenize(self, code : str) -> Iterator[Token]:
        """
        tokenize the code

        """
        for line in code.splitlines():
            line = line.strip()
            for word in line.split():
                if word.isnumeric():
                    yield Token(int(word), TYPE['NUMBER'])
                elif word in SYMBOL._member_names_:
                    yield Token( SYMBOL[word], TYPE['SYMBOL'])
                elif word in OPERATOR._member_names_:
                    yield Token( OPERATOR[word], TYPE['OPERATOR'])
                else:
                    yield Token( word, TYPE['IDENTIFIER'])
            yield Token('\n', TYPE['IDENTIFIER'])
            self.line_nr += 1

    def parse_expression(self) -> bool:
        """
        <expression> = <value> [ <operator> <expression> ]
        <operator> = "+" | "-" | "*" | "/"
        <value> = number | identifier
        """

        if self.curtoken.type == TYPE['NUMBER']:
            self.push_to_stack(self.curtoken.value)
        elif self.curtoken.type is TYPE['IDENTIFIER']:
            self.push_to_stack(self.identifiers[self.curtoken.value])
        else:
            raise ValueError("Odoti <value> [ <operator> <expression> ] mut tuli " + str(self.curtoken))

        try:
            self.next_token()
            if self.curtoken.type == TYPE['OPERATOR']:
                operator = self.curtoken.value
                self.next_token()
                self.parse_expression()

                if operator == OPERATOR['+']:
                    result = self.pop_from_stack() + self.pop_from_stack()
                    self.push_to_stack(result)
                elif operator == OPERATOR['-']:
                    v1 = self.pop_from_stack()
                    v2 = self.pop_from_stack()
                    result = v2 - v1
                    self.push_to_stack(result)
                else:
                    raise ValueError('Mikä operaatori tää muka o ' + str(self.curtoken))
        except StopIteration:
            return True
        return True

    def parse_print_statement(self) -> bool:
        """
        <print_statement> = "san" <expression>
        """

        self.next_token()

        self.parse_expression()
        print("se o " + str(self.pop_from_stack()))
        return True

    def parse_assignment(self) -> bool:
        """
        <assignment> = identifier "o" <expression>
        """

        identifier = self.curtoken.value

        self.next_token()
        if self.curtoken.value != SYMBOL['o']:
            raise ValueError("Odoti 'o' mut tuli " + str(self.curtoken))

        self.next_token()
        self.parse_expression()
        self.identifiers[identifier] = self.pop_from_stack()
        return True

    def parse_function_definition(self) -> bool:
        """
        <function> = "määrittel" identifier \n [ <statement> ... ] "loppu" "\n"
        """
        identifier = self.next_token().value
        if self.next_token().value != '\n':
            raise ValueError("Odoti uut rivii mut tuli " + str(self.curtoken))
        function_tokens = []
        while self.next_token().value != SYMBOL['loppu']:
            function_tokens.append(self.curtoken)
        self.identifiers[identifier] = function_tokens

        self.next_token()
        return True

    def call_function(self) -> bool:

        identifier = self.next_token().value
        if identifier not in self.identifiers:
            raise ValueError("Mikä tääki o olevinas " + str(identifier))

        subfunction = Porilang()
        subfunction.tokens = iter(self.identifiers[identifier])
        subfunction.parse_program()
        self.next_token()

    def parse_statement(self) -> bool:
        """
        <statement> = (<print_statement> | <assignment>) "\n"
        """

        if self.curtoken.value == SYMBOL['san']:
            self.parse_print_statement()
        elif self.curtoken.value == SYMBOL['määrittel']:
            self.parse_function_definition()
        elif self.curtoken.value == SYMBOL['tees']:
            self.call_function()
        else:
            self.parse_assignment()

        if self.curtoken.value != '\n':
            raise ValueError("Odoti uut rivii mut tuli " + str(self.curtoken))
        return True

    def parse_program(self) -> bool:
        """
        <program> = <statement> [ <statement> ... ]
        """
        try:
            while True:
                self.next_token()
                self.parse_statement()
        except StopIteration:
            return True

    def run(self, code) -> bool:
        print("eläk sääki viä")
        self.tokens = self.tokenize(code)
        self.parse_program()
        print("ei mittää")
        return True

if __name__ == '__main__':

    with open('test.pori','r',encoding='UTF-8') as f:
        data = f.read()


    porilang = Porilang()
    porilang.run(data)
