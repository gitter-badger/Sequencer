import ply.lex as lex
import ply.yacc as yacc
import sympy

from constructs import *


class Lexer():
    def __init__(self):
        self.lexer = lex.lex(module=self)
        
    tokens = ("IDENTIFIER", "NUMBER")
    literals = list("=()+-*/^\n;")

    t_IDENTIFIER = r"[a-zA-Z_]\w*"
    t_NUMBER = r"[1-9][0-9]*|0"

    t_ignore = '\t '

    def t_error(self, t):
        exit("Syntax error at '{}'".format(t.value))

    
class Parser():
    def __init__(self):
        self.tokens = Lexer.tokens
        self.lexer = Lexer().lexer
        self.parser = yacc.yacc(module=self)

    def p_program(self, p):
        r"""program : statements
                    | empty"""
        p[0] = p[1] or []


    def p_statements(self, p):
        r"""statements : statements '\n' statement
                       | statements ';' statement
                       | statement"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]

    def p_empty(self, p):
        """empty :"""
        pass

    def p_statement(self, p):
        """statement : sequence_assignment
                     | expression_statement"""
        p[0] = p[1]

    def p_sequence_assignment(self, p):
        """sequence_assignment : variable '(' expression ')' '=' expression"""
        p[0] = SequenceAssignment(p[1], p[3], p[6])

    def p_expression_statement(self, p):
        """expression_statement : expression"""
        p[0] = ExpressionStatement(p[1])

    def p_expression(self, p):
        """expression : arith_expr"""
        p[0] = p[1]

    def p_arith_expr(self, p):
        """arith_expr : term '+' arith_expr
                      | term '-' arith_expr
                      | term"""
        if len(p) == 2:
            p[0] = p[1]
        elif p[2] == '+':
            p[0] = BinaryOp(p[1], p[3], lambda x,y: x+y)
        elif p[2] == '-':
            p[0] = BinaryOp(p[1], p[3], lambda x,y: x-y)

    def p_term(self, p):
        """term : factor '*' term
                | factor '/' term
                | factor '%' term
                | factor"""
        if len(p) == 2:
            p[0] = p[1]
        elif p[2] == '*':
            p[0] = BinaryOp(p[1], p[3], lambda x,y: x*y)
        elif p[2] == '/':
            p[0] = BinaryOp(p[1], p[3], lambda x,y: x/y)

    def p_factor(self, p):
        """factor : '-' factor
                  | power"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = UnaryOp(p[2], lambda x: -x)

    def p_power(self, p):
        """power : atom '^' factor
                 | atom"""
        if len(p) == 2:
            p[0] = p[1]
        elif p[2] == '^':
            p[0] = BinaryOp(p[1], p[3], lambda x,y: x**y)

    def p_atom(self, p):
        """atom : variable
                | number
                | function_call"""
        p[0] = p[1]

    def p_variable(self, p):
        """variable : IDENTIFIER"""
        p[0] = Variable(p[1])

    def p_number(self, p):
        """number : NUMBER"""
        p[0] = Number(p[1])

    def p_function_call(self, p):
        """function_call : variable '(' expression ')'"""
        p[0] = FunctionCall(p[1], [p[3]])

    def p_error(self, p):
        if p is None:
            exit("Syntax error")
        else:
            exit("Syntax error at '{}'".format(p.value))


if __name__ == "__main__":
    parser = Parser().parser
    results = parser.parse("a(n^2) = n")
    env = Environment()

    env = results[0].evaluate(env)
    
    print([env['a'].get_element(env, n) for n in range(1, 100)])
