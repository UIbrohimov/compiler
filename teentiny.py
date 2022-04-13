from lex import *

def main():
    input = "+- */"
    lexer = Lexer(input)

    token = lexer.getToken()
    while token.kind != TokenType.EOF:
        print(token)
        token = lexer.getToken()

main()
