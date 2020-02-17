import string
UPPER_CASE = set(string.ascii_uppercase)

class Location:
    def __init__(self, line, col):
        self.col = col
        self.line = line


class TokenKind:
    ID = 0   # identifier
    LPAR = 1 # (
    RPAR = 2 # )
    NOT = 3  # !
    AND = 4  # /\
    OR = 5   # \/
    IMPLIES = 6  # =>
    IFF = 7  # <=>
    COMMA = 8 # ,

class Token:
    def __init__(self, loc, kind, idStr = ""):
        self.loc = loc
        self.kind = kind
        self.idString = idStr

    def __str__(self):
        if self.kind == TokenKind.ID:
            return "ID(" + self.idString + ")"
        elif self.kind == TokenKind.LPAR:
            return "LPAR"
        elif self.kind == TokenKind.RPAR:
            return "RPAR"
        elif self.kind == TokenKind.NOT:
            return "NOT"
        elif self.kind == TokenKind.AND:
            return "AND"
        elif self.kind == TokenKind.OR:
            return "OR"
        elif self.kind == TokenKind.IMPLIES:
            return "IMPLIES"
        elif self.kind == TokenKind.IFF:
            return "IFF"
        elif self.kind == TokenKind.COMMA:
            return "COMMA"


class Lexer:
    def __init__(self, text):
        self.text = text
        self.line = 1
        self.col = 1

    def tokenize(self):
        current_match = None

        TokenList = []
        TokenArray = []
        IdentifierString = ""

        # for each line of text
        for line in self.text:
            # for each char in the line
            for c in line:

                # end of an ID
                if not c.isalpha() and current_match == TokenKind.ID:
                    current_match = TokenKind.ID
                    TokenList.append(Token(Location(self.line, self.col), TokenKind.ID))
                    TokenList[-1].idString = IdentifierString[:]
                    IdentifierString = ""

                # space
                if c == ' ':
                    current_match = None

                # end of line
                elif c == '\n':
                    current_match = None
                    self.line += 1
                    self.col = 0
                    TokenArray.append(list(TokenList))
                    TokenList[:] = []

                # ID
                elif c.isalpha():
                    current_match = TokenKind.ID
                    IdentifierString += c

                # LPAR
                elif c == '(':
                    current_match = TokenKind.LPAR
                    TokenList.append(Token(Location(self.line, self.col), TokenKind.LPAR))

                # RPAR
                elif c == ')':
                    current_match = TokenKind.RPAR
                    TokenList.append(Token(Location(self.line, self.col), TokenKind.RPAR))

                # NOT
                elif c == '!':
                    current_match = TokenKind.NOT
                    TokenList.append(Token(Location(self.line, self.col), TokenKind.NOT))

                # AND
                elif c == '/':
                    if current_match == TokenKind.OR:
                        current_match = None
                    else:
                        current_match = TokenKind.AND
                        TokenList.append(Token(Location(self.line, self.col), TokenKind.AND))

                # OR
                elif c == '\\':
                    if current_match == TokenKind.AND:
                        current_match = None
                    else:
                        current_match = TokenKind.OR
                        TokenList.append(Token(Location(self.line, self.col), TokenKind.OR))

                # IMPLIES
                elif c == '=':
                    if current_match == TokenKind.IFF:
                        current_match = TokenKind.IFF
                    else:
                        current_match = TokenKind.IMPLIES
                        TokenList.append(Token(Location(self.line, self.col), TokenKind.IMPLIES))

                # IFF
                elif c == '<':
                    current_match = TokenKind.IFF
                    TokenList.append(Token(Location(self.line, self.col), TokenKind.IFF))

                elif c == '>':
                    current_match = None

                # COMMA
                elif c == ',':
                    current_match = TokenKind.COMMA
                    TokenList.append(Token(Location(self.line, self.col), TokenKind.COMMA))

                self.col += 1

        # at the end of file
        else:
            if current_match == TokenKind.ID:
                TokenList.append(Token(Location(self.line, self.col), TokenKind.ID))
                TokenList[-1].idString = IdentifierString[:]
                IdentifierString = ""

            TokenArray.append(list(TokenList))
            TokenList[:] = []

        return TokenArray
