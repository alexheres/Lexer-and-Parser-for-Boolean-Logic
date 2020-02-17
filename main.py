import unittest
from lexer import Lexer, TokenKind
from parse import Parser
from InfixToPostfix import InfixToPostfix


class Test(unittest.TestCase):
    def test(self):
        # ask user for file name and open it
        filename = raw_input("Please enter the Filename: ")
        testFile = open(filename, "r")

        # tokenize input into 2D list
        tokenArray = Lexer(testFile).tokenize()

        inputNum = 1
        for tokenRow in tokenArray:
            # write the lexer string
            lexerString = "Input #" + str(inputNum) + ":\n----------\nLexer: [ "
            for token in tokenRow:
                lexerString += token.__str__()
                if token != tokenRow[-1]:
                    lexerString += ", "

            print(lexerString + " ]")

            parseTree = Parser()
            parseTree.parse(tokenRow)

            # check if parser detected a syntax error
            if parseTree.isValidParse():
                # build and print prefix string
                parseTree.prefixParse = Parser().parse(tokenRow)
                prefixString = "Parser: [ "
                for element in parseTree.prefixParse:
                    prefixString += element
                    if element != parseTree.prefixParse[-1]:
                        prefixString += ", "

                print(prefixString + " ]")

                # convert lexer output from infix to postfix notation
                postfixExpr = InfixToPostfix().ConvertToPostfix(tokenRow)

                # build and print postfix notation
                postfixString = "Postfix: [ "
                for tok in postfixExpr:
                    postfixString += tok.__str__()
                    if tok != postfixExpr[-1]:
                        postfixString += ", "

                print(postfixString + " ]")

                # use postfix notation to write pysmt code and execute it to print satisfiability
                execfile(InfixToPostfix().pysmtEvalution(postfixExpr, inputNum))

                print("\n")

            else:
                parseTree.printError()

            inputNum += 1

        testFile.close()


if __name__ == '__main__':
    unittest.main()
