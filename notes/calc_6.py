# I am going to write the entire code that I have written so far from scratch
# Repitiion is Pratice and practice makes one perfect

INTEGER, PLUS, MINUS, MULTIPLY, DIVIDE, PAREN_OP, PAREN_CL, EOF = 'INT', '+', '-', '*', '/', '(' , ')', 'EOF'

class Token():
    
    def __init__(self,value,type):

        self.value = value
        self.type = type

    def __str__(self):

        return (f'Token has {self.type} of {self.value}')
        
    def __repr__(self):

        return self.__str__()

class Interpreter():

    def __init__(self,text):

        self.text = text
        self.pos = 0
        self.current_token = self.get_next_token()

    def error(self):

        raise Exception ('Input Expression not as expected')

    def get_next_token(self):

        if self.pos >= len(self.text):
            return Token(None,EOF)

        if self.text[self.pos].isspace():
            while self.text[self.pos].isspace():
                self.pos +=1

        if self.text[self.pos].isdigit():
            number = self.get_integer()
            #print (number)
            return Token (number, INTEGER)

        if self.text[self.pos] == PLUS:
            operator = self.text[self.pos]
            self.pos += 1
            #print (operator)
            return Token (operator,PLUS)

        if self.text[self.pos] == MINUS:
            operator = self.text[self.pos]
            self.pos += 1
            return Token (operator, MINUS)

        if self.text[self.pos] == MULTIPLY:
            operator = self.text[self.pos]
            self.pos += 1
            return Token (operator, MULTIPLY)

        if self.text[self.pos] == DIVIDE:
            operator = self.text[self.pos]
            self.pos += 1
            return Token (operator, DIVIDE)

        if self.text[self.pos] == PAREN_OP:
            operator = self.text[self.pos]
            self.pos += 1
            return Token (operator, PAREN_OP)

        if self.text[self.pos] == PAREN_CL:
            operator = self.text[self.pos]
            self.pos += 1
            return Token (operator, PAREN_CL)

        self.error()

    def get_integer(self):
        number = ''
        while self.pos < len(self.text) and self.text[self.pos].isdigit() :
            number += self.text[self.pos]
            self.pos += 1
        return int(number)

    def eat(self, token_type):

        if (self.current_token.type == token_type):
            eat_value = self.current_token.value
            self.current_token = self.get_next_token()
            return eat_value
        else:
            self.error()

    def factor(self):

        if self.current_token.type == INTEGER:
            return int(self.eat(INTEGER))
        
        elif self.current_token.type == PAREN_OP:
            self.eat(PAREN_OP)
            expression = self.sub_expr()
            self.eat(PAREN_CL)
            return expression
        
    def term(self):
        
        left = self.factor()

        while (self.current_token.type in (MULTIPLY, DIVIDE)):

            op = self.eat(self.current_token.value)            

            match(op) :
                case('*'): left *= self.factor()
                case('/'): left /= self.factor()
        return int(left)

    def sub_expr(self):
        
        left = self.term()

        while (self.current_token.type in (PLUS, MINUS)):

            op = self.eat(self.current_token.value)            

            match(op) :
                case('+'): left += self.term()
                case('-'): left -= self.term()

        return int(left)

    def expr(self):

        result = self.sub_expr()

        if self.current_token.type !=EOF:
            self.error()
        else :
            return result

def main():

    #take input string
    while True:
        try:
            text = input('calc>')
        except EOFError:
            print('Exiting Code')
            break

        if (not text):
            continue

        #Interpret Input string
        a = Interpreter(text)

        #get the result of input expression
        print (a.expr())

if __name__ == '__main__':
    main()

