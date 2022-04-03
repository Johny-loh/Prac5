import math
from lexer import Lexer

class RPN(Lexer):
    def __init__(self):
        super().__init__()
        self.FUNC2 = {
                '+' : lambda x, y: x + y,
                '/' : lambda x, y: y / x,
                '-' : lambda x, y: x - y,
                '*' : lambda x, y: x * y,
                '^' : lambda x, y: y ** x}
        self.FUNC1 = {
                'um' : lambda x: -x,
                'sin' : lambda x: math.sin(x),
                'cos' : lambda x: math.cos(x),
                'tg' : lambda x: math.tan(x),
                'ctg' : lambda x: 1 / math.tan(x),
                'ln' : lambda x: math.log(x),
                'exp' : lambda x: math.exp(x)}
        self.PRIORITY = {'+' : 1, '-' : 1, '*' : 2, '/' : 2, '^' : 3}

    def RPN(self):
        buffer = []
        result = []

        for lex in self.divide(self.expression):

            if lex == 'x' or isinstance(lex, float):
                result.append(lex)

                if len(buffer) != 0 and buffer[-1] == 'um':
                    result.append(buffer.pop())

            elif lex in self.FUNC1:
                buffer.append(lex)

            elif lex in self.PRIORITY.keys():
                while (len(buffer) != 0) and (buffer[-1] in self.PRIORITY.keys()) and (self.PRIORITY[buffer[-1]] >= self.PRIORITY[lex]):
                    result.append(buffer.pop())

                buffer.append(lex)

            elif lex == '(':
                buffer.append('(')
            
            elif lex == ')':
                while (len(buffer) != 0) and (buffer[-1] != '('):
                    result.append(buffer.pop())

                buffer.pop()

                if len(buffer) != 0 and buffer[-1] in self.FUNC1:
                    result.append(buffer.pop())

        while len(buffer) != 0:
            result.append(buffer.pop())

        self.lexems = result

        return result
