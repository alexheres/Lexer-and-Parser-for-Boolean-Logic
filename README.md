# Lexer-and-Parser-for-Boolean-Logic

# -------- Program and Functionalities ---------

The program takes as input a text file, where each line is a boolean statement. As long as the syntax is correct, the program uses the pySMT library to determine whether or not boolean statements are Satisfiable (see here for more info on Boolean Satisfiability: https://en.wikipedia.org/wiki/Boolean_satisfiability_problem)

# -------- Lexer and Parser ---------

The tokens used for the lexical analyzer are as follows:<br><br>
    ID = [A-Z]+ <br>
    LPAR = ( <br>
    RPAR = ) <br>
    NOT = ! <br>
    AND = /\ <br>
    OR = \/ <br>
    IMPLIES = ‘=>’ <br>
    IFF = ‘<=>’ <br>
    COMMA = , <br>
<br>
And this is the grammar which the parser follows, where the starting variable is propositions: <br><br>
    propositions -> proposition more-proposition  <br> 
    more-proposition -> , propositions | e <br>
    proposition -> atomic | compound <br>
    atomic -> 0 | 1 | ID <br>
    compound -> atomic connective proposition | LPAR proposition RPAR | NOT proposition <br>
    connective -> AND | OR | IMPLIES | IFF <br>


# -------- Program Input ---------

The program prompts the user for a text file, where each line in the file is a boolean statement. The program solves the Satisfiability problem for each statement, and returns each result in the console. 

Given our tokens and grammar, the program emulates a preorder parse tree traversal to check if a given boolean statement is valid. Then,  an infix to postfix conversion algorithm is used to deduce the correct order of operations needed to accurately calculate Satisfiability.


For example, the following can be a valid line of input:
( P \/ Q ) , ( X => Y )

Whereas the next line of input is invalid, and would produce a syntax error:
!Q)P!
