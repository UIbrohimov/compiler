from lex import *

def main():
    input = "+-123 9.8654*/"
    lexer = Lexer(input)

    token = lexer.getToken()
    while token.kind != TokenType.EOF:
        print(token)
        token = lexer.getToken()

main()
