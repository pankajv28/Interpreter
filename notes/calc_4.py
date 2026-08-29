# define various token types
INTEGER, PLUS, MINUS, MULTIPLY, DIVIDE, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MULTIPLY' , 'DIVIDE' ,'EOF'

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
        self.current_token = None

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
        factor_integer = self.current_token.value
        self.eat(INTEGER)
        #print (factor_integer)
        return factor_integer


    def expr(self):

        self.current_token = self.get_next_token()

        left = self.factor()

        while self.current_token.type in ('PLUS','MINUS','MULTIPLY','DIVIDE'):

            op = self.current_token.value
            self.eat(self.current_token.type)

            match op:
                case '+':
                    left = left + self.factor()
                case '-':
                    left = left - self.factor()
                case '*':
                    left = left * self.factor()
                case '/':
                    left = int(left / self.factor())

        return left
    
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