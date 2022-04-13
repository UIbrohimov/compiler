import enum
import sys

class Lexer:
    def __init__(self, input):
        self.source = input + '\n'
        self.curChar = ''
        self.curPos = -1
        self.nextChar()

    # Process the next character
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0' # EOF
        else:
            self.curChar = self.source[self.curPos]

    # Return the lookahead character
    def peekChar(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos + 1] 

    # Invalid token found, print error message and exit
    def abort(self, message):
        sys.exit("Lexing error: " + message)

    def skipWhitespace(self):
        """
        Skip whitespace except newlines, which we will 
        use to indecate the end of a statement
        """
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    # Skip comments in the code
    def skipComments(self):
        if self.curChar == "#":
            while self.curChar != '\n':
                self.nextChar() 

    # Return the next token
    def getToken(self):
        """
        Check the first character of this token to see if 
        we can decide what is it.
        If it is a multiple character operator (e.g., !=),
        number identifier, or string, then we need to 
        process the whole token.
        """
        self.skipWhitespace()
        self.skipComments()
        token = None
        if self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)

        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)

        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)

        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)

        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)

        elif self.curChar == '\0':
            token = Token('', TokenType.EOF)

        elif self.curChar == '=':
            # check whether this token is = or ==
            if self.peekChar() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)

        elif self.curChar == '>':
            # Check whether this is token is > or >=
            if self.peekChar() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)

        elif self.curChar == '<':
            # Check whether this is token is < or <=
            if self.peekChar() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)

        elif self.curChar == '!':
            if self.peekChar() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peekChar())

        elif self.curChar == '\"':
            # Get characters between quotations.
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\"':
                # Don't allow special characters in the string. No escape characters, newlines, tabs, or %.
                # We will be using C's printf on this string.
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal character in string.")
                self.nextChar()

            tokText = self.source[startPos : self.curPos] # Get the substring.
            token = Token(tokText, TokenType.STRING)

        elif self.curChar.isdigit():
            # Leading character is a digit, so this must be a number.
            # Get all consecutive digits and decimal if there is one.
            startPos = self.curPos
            while self.peekChar().isdigit():
                self.nextChar()

            if self.peekChar() == '.': # Decimal!
                self.nextChar()

                # Must have at least one digit after decimal.
                if not self.peekChar().isdigit(): 
                    # Error!
                    self.abort("Illegal character in number.")
                while self.peekChar().isdigit():
                    self.nextChar()

            tokText = self.source[startPos : self.curPos + 1] # Get the substring.
            token = Token(tokText, TokenType.NUMBER)

        else:
            # Unknown token!
            self.abort("Unknown token: " + self.curChar)

        self.nextChar()
        return token


class Token:
    """
    Token contains the original text and the type of token
    """
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText # original text
        self.kind = tokenKind # token type

    def __str__(self):
        return f'Token({self.text}, {self.kind})'

    def __repr__(self):
        return self.__str__()


class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    INDENT = 2
    STRING = 3

    # KEYWORDS
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111

    # OPERATORS
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
