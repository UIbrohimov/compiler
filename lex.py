import sys
import enum

# Lexer object keeps track of current position in the source code and produces each token.
# Lexer obyekt kompaylerning har bir turgan yerini belgilaydi va coddagi tokenlarni obrobotka qiladi
class Lexer:
    def __init__(self, input):
        self.source = input + '\n' # Lexerga string ko'rinishidagi kod. Parse qilish osonroq bo'lishi uchun oxiriga \n qo'yib ketamiz.
        self.curChar = ''   # Berilgan string ko'rinishidagi source coddagi hoizirgi simvol.
        self.curPos = -1    # Keyingi kutilayotgan simvol.
        self.nextChar()

    # Keyingi simvolni olish.
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0'  # EOF
        else:
            self.curChar = self.source[self.curPos]

    # Oldinda turgan simvolni aniqlash.
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos+1]

    # Noto'g'ri sintaksisga duch kelgan taqdirda kerakli ogohlantiruv 
    # xabarini berib, interpritatorni to'xtatish.
    def abort(self, message):
        sys.exit("Leksik xato. " + message)

    # Tokenni qaytarish.
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None

        # Kelgan stringdagi birinchi elementni tekshrish, shunga qarab keyingi qadam tashlanadi.
        if self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == '=':
            # Token = yoki == ekanligini tekshirish
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == '>':
            # Token > yoki >= ekanligini tekshirish
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == '<':
            # Token < yoki <= ekanligini tekshirish
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)
        elif self.curChar == '!':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())

        elif self.curChar == '\"':
            # Qo'shtirnoq ichidagi belgilarni olish.
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\"':
                # Don't allow special characters in the string. No escape characters, newlines, tabs, or %.
                # Biz bu stringni print qilish uchn C ning printf funksiyasidan foydalanim.
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal character in string.")
                self.nextChar()

            tokText = self.source[startPos : self.curPos] # Get the substring.
            token = Token(tokText, TokenType.STRING)

        elif self.curChar.isdigit():
            # Birinchi harf bu son, Demak bu raqam bo'lishi mumkin.
            # Barcha ketma ket sonlarni olamiz yoki o'nli sanoq sistemasi ekanligini aniqlaymiz.
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == '.': # Decimal!
                self.nextChar()

                # O'nli qismidan keyin kamida bitta son bo'lishi kerak.
                if not self.peek().isdigit(): 
                    # Xato!
                    self.abort("Illegal character in number.")
                while self.peek().isdigit():
                    self.nextChar()

            tokText = self.source[startPos : self.curPos + 1] # Get the substring.
            token = Token(tokText, TokenType.NUMBER)
        elif self.curChar.isalpha():
            # Birinchi simvol harf, demak bu kalit so'z yoki biror kerakli simvol.
            # Barcha harf va raqamlarni ajratib olamiz.
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()

            # Check if the token is in the list of keywords.
            tokText = self.source[startPos : self.curPos + 1] # Get the substring.
            keyword = Token.checkIfKeyword(tokText)
            if keyword == None: # Belgi
                token = Token(tokText, TokenType.IDENT)
            else:   # kalit so'z
                token = Token(tokText, keyword)
        elif self.curChar == '\n':
            # Yangi qator.
            token = Token('\n', TokenType.NEWLINE)
        elif self.curChar == '\0':
             # EOF - End Of a File.
            token = Token('', TokenType.EOF)
        else:
            # Unknown token!
            self.abort("Unknown token: " + self.curChar)

        self.nextChar()
        return token

    # Bo'sh joy va commentariyalarni ignore qilish, biror amalning tugashini bildira olish uchun.
    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    def skipComment(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()


# Token class tokenning matni va uning turini saqlaydi.
class Token:   
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText   # Tokenning asl matni. Belgilar, string va raqamlar uchun.
        self.kind = tokenKind   # Token type bu tokenning klasifikatsiyasi yani tipi.

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # Keyvor bo'lishi uchun tanlov raqami 100 va 200 ning orasida bo'lishi kerak.
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None


# Token type binning kichik dasturlash tilimizdagi barcha tokenlar uchun raqamli choice class.
class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Kalit so'zlar.
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
    # Operatorlar.
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
