import sys
from lex import *


class Parser:
    """
    Parser object keeps track of current token
    and checks if the node matches the grammar
    """

    def __init__(self, lexer):
        pass

    # return true if the current token matches
    def checkToken(self, kind):
        pass

    # return true if the next token matches
    def checkPeek(self, kind):
        pass

    # try to match current token.
    # if not, error, Advances the current token
    def match(self, kind):
        pass

    # advances the current token
    def nextToken(self):
        pass

    def abort(self, message):
        sys.exit("Error: " + message)
