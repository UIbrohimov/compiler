from lex import *
from parse import *

def main():
    print("Teeny Tiny Compiler")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as an argument\nUsage: python3 teentiny.py <filename>")
    with open(sys.argv[1], 'r') as sourceFile:
        source = sourceFile.read()
    
    # initialize the lexer and parser
    lexer = Lexer(source)
    parser = Parser(lexer)

    parser.program()
    print("\n\nParsing completed.")

main()
