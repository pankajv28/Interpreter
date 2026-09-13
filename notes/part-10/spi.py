import sys

""" SPI - Simple Pascal Interpreter """

###############################################################################
#                                                                             #
#  LEXER                                                                      #
#                                                                             #
###############################################################################

# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, MUL, INTEGER_DIV, FLOAT_DIV, LPAREN, RPAREN, EOF, DOT, SEMI, BEGIN, END, ASSIGN, ID, COLON, REAL, INTEGER_CONST, REAL_CONST,COMMA, PROGRAM, VAR = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '/', '(', ')', 'EOF', 'DOT', 'SEMI', 'BEGIN', 'END', 'ASSIGN', 'ID', 'COLON', 'REAL', 'INTEGER_CONST', 'REAL_CONST', 'COMMA', 'PROGRAM', 'VAR'
)


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return (f'Token({self.type}, {self.value})')
    
    def __repr__(self):
        return self.__str__()


class Lexer(object):

    RESERVED_KEYWORDS = {
        'BEGIN' : Token('BEGIN','BEGIN'),
        'END' : Token('END','END'),
        'DIV' : Token('DIV', 'DIV'),
        'INTEGER' : Token('INTEGER','INTEGER'),
        'REAL' : Token ('REAL','REAL'),
        'PROGRAM' : Token ('PROGRAM','PROGRAM'),
        'VAR' : Token ('VAR', 'VAR')
    }
        
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        if self.pos < len(self.text) - 1:
            return self.text[self.pos + 1]
        else :
            return None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '}':
            self.advance()
        self.advance()

    def number(self):
        """Return a (multidigit) integer or float value consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result+=self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                    result += self.current_char
                    self.advance()

            return Token(REAL_CONST,float(result))
        else:
            return Token(INTEGER_CONST, int(result))

    def _id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum() or self.current_char == '_':
            result += self.current_char
            self.advance()
        result = result.upper()
        token = self.RESERVED_KEYWORDS.get(result, Token(ID,result))
        return (token)
        
    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:


            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '{':
                self.advance()
                self.skip_comment()
                continue

            if self.current_char.isalpha() or self.current_char == '_':
                return self._id()

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN,':=')

            if self.current_char == ';' :
                self.advance()
                return Token(SEMI,';')

            if self.current_char == ':' :
                self.advance()
                return Token(COLON,':')

            if self.current_char == ',' :
                self.advance()
                return Token(COMMA,',')            

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(FLOAT_DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '.' :
                self.advance()
                return Token(DOT,'.')

            self.error()

        return Token(EOF, None)


###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

class AST(object):
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class UnaryOp(AST):
    def __init__(self,op,operand):
        self.token = self.op = op
        self.operand = operand

class Compound(AST):
    def __init__(self):
        self.children = []

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(AST):
    def __init__(self,token):
        self.token = token
        self.value = token.value

class NoOp(AST):
    pass

class Program(AST):
    def __init__(self,name, block):
        self.name = name
        self.block = block

class Block(AST):
    def __init__(self,declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement

class VarDecl(AST):
    def __init__(self,var_node,type_node):
        self.var_node = var_node
        self.type_node = type_node

class Type(AST):
    def __init__(self,token):
        self.token = token
        self.value = token.value


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def program(self):
        self.eat(PROGRAM)
        name_node = self.variable()
        self.eat(SEMI)
        block_node = self.block()
        self.eat(DOT)
        program_node = Program(name_node.value,block_node)
        return program_node

    def block(self):
        declaration_node = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_node, compound_statement_node)
        return node

    def declarations(self):
        declarations = []
        if self.current_token.type == VAR:
            self.eat(VAR)
            while (self.current_token.type == ID):
                declarations.extend(self.var_declarations())
                self.eat(SEMI)
        return declarations

    def var_declarations(self):
        var_nodes = [Var(self.current_token)]
        self.eat(ID)

        while self.current_token.type == COMMA : 
            self.eat(COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(ID)

        self.eat(COLON)

        type_node = self.type_spec()

        var_declarations = [
                VarDecl(node,type_node)
                for node in var_nodes
                ]
        
        return var_declarations

    def type_spec(self):
        token = self.current_token
        if self.current_token.type == INTEGER :
            self.eat(INTEGER)
        elif self.current_token.type == REAL:
            self.eat(REAL)
        node = Type(token)
        return node

    def compound_statement(self):
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root
    
    def statement_list(self):

        node = self.statement()
        result  = [node]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            result.append(self.statement())
        return result
    
    def statement(self):
        if self.current_token.type == BEGIN : 
            node = self.compound_statement()
        elif self.current_token.type == ID : 
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node
    
    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left,token,right)
        return node

    def variable(self):
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        node = NoOp()
        return node

    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, INTEGER_DIV, FLOAT_DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == INTEGER_DIV:
                self.eat(INTEGER_DIV)
            elif token.type == FLOAT_DIV:
                self.eat(FLOAT_DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def factor(self):
        """factor : INTEGER | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type in (INTEGER_CONST, REAL_CONST):
            self.eat(token.type)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type in (PLUS,MINUS):
            op = token
            self.eat(token.type)
            return UnaryOp(op,self.factor())
        elif token.type == ID:
            return self.variable()
        
    def parse(self):
        node = self.program()
        if self.current_token.value is None:
            return node
        else :
            return self.error()

###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):

    GLOBAL_SCOPE = {}

    def __init__(self, parser):
        self.parser = parser
    def visit_Program(self,node):
        self.visit(node.block)

    def visit_Block(self,node):
        for declaration in node.declarations :
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDecl(self,node):
        pass

    def visit_Type(self,node):
        pass

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == INTEGER_DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == FLOAT_DIV:
            return float(self.visit(node.left)) / float(self.visit(node.right))

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self,node):
        if node.op.type == PLUS :
            return self.visit (node.operand)
        elif node.op.type == MINUS :
            return -self.visit (node.operand)

    def visit_Compound(self,node):
        for child in node.children:
            self.visit(child)

    def visit_Assign(self,node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)
    
    def visit_Var(self,node):
        var_name = node.value
        var_val = self.GLOBAL_SCOPE.get(var_name)
        if var_val is None : 
            raise NameError(f'{var_name} doesnt have a value')
        else : 
            return var_val
    
    def visit_NoOp(self,node):
        pass

    def interpret(self):
        tree = self.parser.parse()
        if tree is None:
            return ''
        return self.visit(tree)

def main():

        text = open(sys.argv[1], 'r').read()

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(interpreter.GLOBAL_SCOPE)


if __name__ == '__main__':
    main()