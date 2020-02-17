from lexer import Token, TokenKind, Location


class InfixToPostfix:
    def __init__(self):
        self.tokenList = []
        self.postfixTokens = []

        # 'stack' variables
        self.stack = []
        self.stackSize = -1

        # operator precedence
        self.priority = {'AND': 1, 'OR': 1, 'IFF': 1, 'IMPLIES': 1, 'NOT': 2}

    def resetStack(self):
        self.stack = []
        self.stackSize = -1

    def isEmpty(self):
        if self.stackSize == -1:
            return True
        else:
            return False

    # peeks at the stack's top-most element
    def top(self):
        return self.stack[-1]

    # pop top-most element from stack, if not empty
    def pop(self):
        if not self.isEmpty():
            self.stackSize -= 1
            return self.stack.pop()

    # push to top of the stack
    def push(self, element):
        self.stackSize += 1
        self.stack.append(element)

    # function to compare operator precedence
    def isLowerPriority(self, inputKind):
        try:
            if self.priority[inputKind] <= self.priority[self.top().kind]:
                return True
            else:
                return False
        # LPAR, RPAR, and ID cases:
        except KeyError:
            return False

    # function to turn COMMAs into ANDs,
    # while appropriately preserving precedence
    def parenthesizeTokens(self):
        newTokenList = []

        newTokenList.append(Token(Location(1, 1), TokenKind.LPAR))

        for tok in self.tokenList:
            # change COMMAs to ANDs, to fix precedence for postfix evaluation
            if tok.kind == TokenKind.COMMA:
                newTokenList.append(Token(Location(1, 1), TokenKind.RPAR))
                newTokenList.append(Token(Location(1, 1), TokenKind.AND))
                newTokenList.append(Token(Location(1, 1), TokenKind.LPAR))
            else:
                newTokenList.append(Token(tok.loc, tok.kind, tok.idString))

        newTokenList.append(Token(Location(1, 1), TokenKind.RPAR))
        return newTokenList

    # function to convert propositions from infix to postfix notation
    def ConvertToPostfix(self, tokenList):
        # build the list of tokens to convert to postfix
        self.tokenList = tokenList
        self.tokenList = self.parenthesizeTokens()

        for token in self.tokenList:
            # ID case - append to postfix string
            if token.kind == TokenKind.ID:
                self.postfixTokens.append(token)

            # LPAR case - push to operator stack
            elif token.kind == TokenKind.LPAR:
                self.push(token)

            # RPAR case - pop from operator stack until either:
            # 1. we reach an LPAR, or
            # 2. the stack is emptied
            elif token.kind == TokenKind.RPAR:
                while not self.isEmpty() and self.top().kind != TokenKind.LPAR:
                    i = self.pop()
                    self.postfixTokens.append(i)

                self.pop()

            # AND, OR, IFF, IMPLIES, and NOT cases - pop from stack until either:
            # 1. the top stack element is an operator of lower precedence, or
            # 2. the stack is emptied
            # Then finally, push operator to stack.
            else:
                while not self.isEmpty() and self.isLowerPriority(token.kind):
                    self.postfixTokens.append(self.pop())
                self.push(token)

        # END - pop all remaining ops from stack, if any
        while not self.isEmpty():
            self.postfixTokens.append(self.pop())

        return self.postfixTokens

    # function to write pysmt code and evaluation satisfiability
    # of a proposition in postfix notation
    def pysmtEvalution(self, postExpr, fileNum):
        # reset the stack and create python file
        self.resetStack()
        file = open("pysmtResult" + fileNum.__str__() + ".py", "w+")

        # import all modules possibly needed
        file.write("from pysmt.shortcuts import Symbol, Not, And, Or, Iff, Implies, is_sat\n\n")

        # find all unique SYMBOLS
        uniqueSymbols = []
        for op in postExpr:
            if op.kind == TokenKind.ID:
                if not uniqueSymbols.__contains__(op.idString):
                    uniqueSymbols.append(op.idString)

        # write all unique SYMBOLS to file
        for sym in uniqueSymbols:
            file.write(sym + " = Symbol(\"" + sym + "\")\n")

        # Evaluate the postfix expression with stack,
        # creating new proposition variables as we go
        propNum = 1
        for op in postExpr:
            # SYMBOL case
            # push to stack
            if op.kind == TokenKind.ID:
                file.write("prop" + propNum.__str__() + " = " + op.idString + "\n")
                self.push("prop" + propNum.__str__())

            else:
                # NOT case
                # pop once, push once
                if op.kind == TokenKind.NOT:
                    file.write("prop" + propNum.__str__() + " = Not(" + self.pop().__str__() + ")\n")
                    self.push("prop" + propNum.__str__())

                # AND, OR, IFF, IMPLIES cases
                # pop twice, push once
                else:
                    var1 = self.pop()
                    var2 = self.pop()
                    file.write("prop" + propNum.__str__() + " = " + str.title(op.__str__()) + "(" + var2 + ", " + var1 + ")\n")

                    self.push("prop" + propNum.__str__())

            propNum += 1

        # satisfiability print statement,
        # pop 'completed' proposition from stack for evaluation
        file.write("print(\"Satisfiability: \" + is_sat(" + self.pop() + ").__str__())\n")
        file.close()
        return "pysmtResult" + fileNum.__str__() + ".py"
