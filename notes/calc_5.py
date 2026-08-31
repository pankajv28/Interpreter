# define various token types
INTEGER, PLUS, MINUS, MULTIPLY, DIVIDE, EOF, OPEN, CLOSE = 'INTEGER', 'PLUS', 'MINUS', 'MULTIPLY' , 'DIVIDE' ,'EOF', 'OPEN', 'CLOSE'

class Token():
    def __init__(self,type,value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token is of type {self.type} and has {self.value}"

    def __repr__(self):
        return self.__str__()

class Interpreter():
    def __init__(self,text):
        self.text = text
        self.pos = 0
        self.current_token = self.get_next_token()

    def error(self):
        raise Exception('Input String not expected')

    def whitespace(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def get_next_token(self):

        text = self.text

        if self.pos > len(text)-1:
            return Token ('EOF',None)

        if text[self.pos].isspace():
            self.whitespace()

        if text[self.pos] == '(':
            current_token = Token('OPEN', text[self.pos])
            self.pos += 1
            return current_token

        if text[self.pos] == ')':
            current_token = Token('CLOSE', text[self.pos])
            self.pos+=1
            return current_token

        if text[self.pos].isdigit():
            current_token = Token('INTEGER',self.get_integer())
            return current_token

        if text[self.pos] == '+':
            current_token = Token('PLUS', text[self.pos])
            self.pos += 1
            return current_token

        if text[self.pos] == '-':
            current_token = Token('MINUS', text[self.pos])
            self.pos += 1
            return current_token      

        if text[self.pos] == '*':
            current_token = Token('MULTIPLY', text[self.pos])
            self.pos += 1
            return current_token    

        if text[self.pos] == '/':
            current_token = Token('DIVIDE', text[self.pos])
            self.pos += 1
            return current_token  
        
        self.error()

    def get_integer(self):
        integer = ''
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            integer = integer + self.text[self.pos]
            self.pos += 1
        return (int(integer))
        
    def eat(self, token_type):

        if self.current_token.type == token_type:
            #print(f'Position {self.pos} has {self.current_token.value} ')
            self.current_token = self.get_next_token()
        else :
            #print(f'Issue at Position {self.pos} has {self.current_token.value} ')
            self.error()

    def factor(self):
        if self.current_token.value == '(':
            self.eat(OPEN)
            priority = self.expr()
            self.eat(CLOSE)
            return priority
        elif self.current_token.type == INTEGER:
            factor_integer = self.current_token.value
            self.eat(INTEGER)
            return factor_integer

    def term(self):

        left_term = self.factor()

        while self.current_token.type in ('MULTIPLY','DIVIDE'):

            op_term = self.current_token.value
            self.eat(self.current_token.type)

            match op_term:
                case '*':
                    left_term *= self.factor()
                case '/':
                    left_term = int(left_term / self.factor())

        return int(left_term)

    def expr(self):

        left_expr = self.term()

        while self.current_token.type in ('PLUS','MINUS'):

            op_expr = self.current_token.value
            self.eat(self.current_token.type)

            match op_expr:
                case '+':
                    left_expr += self.term()
                case '-':
                    left_expr -= self.term()

        return int(left_expr)

def main():

    while True:
        try:
            input_str = input('calc>>')
        except EOFError:
            break
        if not input_str:
            continue
        calculation = Interpreter(input_str)
        print (calculation.expr())

if __name__ == '__main__':
    main()