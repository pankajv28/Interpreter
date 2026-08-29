# define various token types
INTEGER, PLUS, MINUS, MULTIPLY, DIVIDE, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MULTIPLY' , 'DIVIDE' ,'EOF'

class Token():
    def __init__(self,type,value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token is of type {self.type} and has {self.value}"

    def __repr__(self):
        self.__str__()

class Interpreter():
    def __init__(self,text):
        self.text = text
        self.pos = 0
        self.current_token = None

    def error(self):
        raise Exception('Input String not expected')

    def get_next_token(self):

        text = self.text

        if self.pos > len(text)-1:
            return Token ('EOF',None)

        current_value = text[self.pos]

        if current_value.isspace():
            self.pos += 1

        if current_value.isdigit():
            current_token = Token('INTEGER',self.get_integer())
            return current_token

        elif current_value == '+':
            current_token = Token('PLUS', current_value)
            self.pos += 1
            return current_token

        elif current_value == '-':
            current_token = Token('MINUS', current_value)
            self.pos += 1
            return current_token      

        elif current_value == '*':
            current_token = Token('MULTIPLY', current_value)
            self.pos += 1
            return current_token    

        elif current_value == '/':
            current_token = Token('DIVIDE', current_value)
            self.pos += 1
            return current_token  
        
        self.error()

    def get_integer(self):
        integer = ''
        while self.pos <= len(self.text)-1 and self.text[self.pos].isdigit():
            integer = integer + self.text[self.pos]
            self.pos += 1
        return (int(integer))
        
    def eat(self, token_type):

        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
            return True
        else :
            return False

    def expr(self):

        self.current_token = self.get_next_token()

        left = int(self.current_token.value)
        self.eat('INTEGER')

        while (self.current_token.type != 'EOF'):

            op = self.current_token.value
            self.eat('PLUS') or self.eat ('MINUS') or self.eat('MULTIPLY') or self.eat('DIVIDE')

            right = int(self.current_token.value)
            self.eat('INTEGER')

            self.eat('EOF')
            match op:
                case '+': left =  left + right
                case '-': left =  left - right
                case '*': left =  left * right
                case '/': left =  int(left / right)

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