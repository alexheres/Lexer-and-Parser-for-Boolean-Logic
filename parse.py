from lexer import Location, Token, TokenKind
import sys


class VariableType:
    PROPOSITIONS = 0
    PROPOSITION = 1
    ATOMIC = 2
    MOREPROPOSITIONS = 3
    COMPOUND = 4
    CONNECTIVE = 5


class Parser:
    def __init__(self):
        self.loc = Location(0, 0)
        self.prefixParse = []
        self.tokenList = []
        self.tokenIndex = 0
        self.error = 0

    def parse(self, tokens):
        self.tokenList = tokens

        self.checkParenthesis(tokens)
        if self.error == 0:
            self.propositions()

        return self.prefixParse

    def match(self, expectedTok):
        if self.tokenList[self.tokenIndex].kind == expectedTok:
            self.prefixParse.append(self.tokenList[self.tokenIndex].__str__())
            self.tokenIndex += 1
        else:
            self.syntaxError(self.tokenList[self.tokenIndex])

    def propositions(self):
        if self.error:
            return
        self.prefixParse.append("propositions")

        self.proposition()
        self.more_proposition()

    def more_proposition(self):
        if self.error:
            return
        self.prefixParse.append("more-proposition")

        if self.inBounds() and self.tokenList[self.tokenIndex].kind == TokenKind.COMMA:
            self.match(TokenKind.COMMA)
            self.propositions()

        else:
            self.prefixParse.append("epsilon")

    def proposition(self):
        if self.error:
            return
        self.prefixParse.append("proposition")

        if (self.tokenList[self.tokenIndex].kind == TokenKind.LPAR or
            self.tokenList[self.tokenIndex].kind == TokenKind.NOT or
            (self.tokenIndex < len(self.tokenList) - 1 and
                self.tokenList[self.tokenIndex].kind == TokenKind.ID and
                self.isConnective(self.tokenList[self.tokenIndex + 1])
            )
        ):
            self.compound()

        elif self.tokenList[self.tokenIndex].kind == TokenKind.ID:
            self.atomic()

        else:
            self.syntaxError(self.tokenList[self.tokenIndex])

    def atomic(self):
        if self.error:
            return
        self.prefixParse.append("atomic")

        self.match(TokenKind.ID)

    def compound(self):
        if self.error:
            return
        self.prefixParse.append("compound")

        if self.tokenList[self.tokenIndex].kind == TokenKind.ID:
            self.atomic()
            self.connective()
            self.proposition()

        elif self.tokenList[self.tokenIndex].kind == TokenKind.LPAR:
            self.match(TokenKind.LPAR)
            self.proposition()
            self.match(TokenKind.RPAR)

        elif self.tokenList[self.tokenIndex].kind == TokenKind.NOT:
            self.match(TokenKind.NOT)
            self.proposition()

        else:
            self.syntaxError(self.tokenList[self.tokenIndex])

    def connective(self):
        if self.error:
            return
        self.prefixParse.append("connective")

        if self.tokenList[self.tokenIndex].kind == TokenKind.AND:
            self.match(TokenKind.AND)
        elif self.tokenList[self.tokenIndex].kind == TokenKind.OR:
            self.match(TokenKind.OR)
        elif self.tokenList[self.tokenIndex].kind == TokenKind.IMPLIES:
            self.match(TokenKind.IMPLIES)
        elif self.tokenList[self.tokenIndex].kind == TokenKind.IFF:
            self.match(TokenKind.IFF)

        else:
            self.syntaxError(self.tokenList[self.tokenIndex])

    def isConnective(self, token):
        if self.error:
            return
        if (token.kind == TokenKind.AND or
            token.kind == TokenKind.OR or
            token.kind == TokenKind.IMPLIES or
            token.kind == TokenKind.IFF):
            return 1
        else:
            return 0

    def inBounds(self):
        if self.tokenIndex < len(self.tokenList):
            return 1
        else:
            return 0

    def checkParenthesis(self, tokenList):
        balance = 0
        lastPar = Token(Location(0, 0), None)
        for token in tokenList:
            if token.kind == TokenKind.LPAR:
                balance += 1
                lastPar = token

            elif token.kind == TokenKind.RPAR:
                balance -= 1
                lastPar = token
                if balance < 0:
                    self.syntaxError(lastPar)
                    return

        if balance != 0:
            self.syntaxError(lastPar)

    def syntaxError(self, token):
        self.prefixParse = ["Syntax Error at line " + str(token.loc.line) + ", column " + str(token.loc.col) + "."]
        self.error = 1
        return

    def isValidParse(self):
        return self.error == 0

    def printError(self):
        print("Parser: " + self.prefixParse.__str__() + "\n\n")
