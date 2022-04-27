from lex import *
from emit import *
from parse import *
import sys

def main():
    print("Mitti kompilyator !")

    if len(sys.argv) != 2:
        sys.exit("Error: Missing source file, usage: python3 teenytiny.py <source_file>.")
    with open(sys.argv[1], 'r') as inputFile:
        input = inputFile.read()

    # Emitter, lexer va parserni initialize qilish.
    lexer = Lexer(input)
    emitter = Emitter("out.c")
    parser = Parser(lexer, emitter)

    parser.program() # Parserni ishga tushirish.
    emitter.writeFile() # Chiquvchi faylni saqlash.
    print("Kompilyatsiya bajarildi.")

main()
