import timeit

import textparser
from textparser import Forward
from textparser import Sequence
from textparser import DelimitedList
from textparser import choice
from textparser import Optional


class Parser(textparser.Parser):

    def token_specs(self):
        return [
            ('SKIP',                r'[ \r\n\t]+'),
            ('NUMBER',              r'-?\d+(\.\d+)?([eE][+-]?\d+)?'),
            ('TRUE',                r'true'),
            ('FALSE',               r'false'),
            ('NULL',                r'null'),
            ('ESCAPED_STRING',      r'"(\\"|[^"])*?"'),
            ('LPAREN',         '(', r'\('),
            ('RPAREN',         ')', r'\)'),
            ('LBRACKET',       '[', r'\['),
            ('RBRACKET',       ']', r'\]'),
            ('LBRACE',         '{', r'\{'),
            ('RBRACE',         '}', r'\}'),
            ('COMMA',          ',', r','),
            ('COLON',          ':', r':'),
            ('MISMATCH',            r'.')
        ]

    def grammar(self):
        value = Forward()
        list_ = Sequence('[', Optional(DelimitedList(value)), ']')
        pair = Sequence('ESCAPED_STRING', ':', value)
        dict_ = Sequence('{', Optional(DelimitedList(pair)), '}')
        value <<= choice(list_,
                         dict_,
                         'ESCAPED_STRING',
                         'NUMBER',
                         'TRUE',
                         'FALSE',
                         'NULL')

        return value


def parse_time(json_string, iterations):
    parser = Parser()

    def _parse():
        parser.parse(json_string)

    return timeit.timeit(_parse, number=iterations)


def parse(json_string):
    return Parser().parse(json_string)


def version():
    return textparser.__version__
