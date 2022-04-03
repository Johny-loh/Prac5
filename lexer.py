from consts import *
from exeptions import LexerException


class Lexer:
    def __init__(self):

        self.state = 'S'
        self.buffer = ''
        self.brackets_count = 0
        self.lexems = []
        self.char = ''

        self.exception = templates

        self.machine = {
            'S': self.state_S,
            'I': self.state_I,
            'R': self.state_R,
            'B': self.state_B,
            'F': self.state_F,
            'X': self.state_X
        }

    def raise_exception(self):
        expected = self.exception[self.state]
        msg = 'Excepted {expected}, but got "{char}"'.format(expected=expected, char=self.char)

        raise LexerException(msg)

    def state_S(self):
        if self.char.isdigit():
            self.buffer += self.char
            return 'I'

        elif self.char == '(':
            self.brackets_count += 1
            self.lexems.append(self.char)
            return 'S'

        elif self.char == '-':
            self.lexems.append('um')
            return 'S'

        elif self.char.isalpha() and self.char != 'x':
            self.buffer += self.char
            return 'F'

        elif self.char == 'x':
            self.lexems.append(self.char)
            return 'X'

        self.raise_exception()

    def state_I(self):
        if self.char.isdigit():
            self.buffer += self.char
            return 'I'
        
        elif self.char in DELIM:
            self.buffer += self.char
            return 'R'

        elif self.char == ')':
            self.brackets_count -= 1
            if self.buffer != '':
                self.lexems.append(self.buffer)
            self.lexems.append(self.char)
            self.buffer = ''
            return 'B'

        elif self.char in OPERARIONS:
            if self.buffer != '':
                self.lexems.append(self.buffer)
            self.lexems.append(self.char)
            self.buffer = ''
            return 'S'
        
        self.raise_exception()
        
    def state_R(self):
        if self.char.isdigit():
            self.buffer += self.char
            return 'R'

        elif self.char == ')':
            self.brackets_count -= 1
            if self.buffer != '':
                self.lexems.append(self.buffer)
            self.lexems.append(self.char)
            self.buffer = ''
            return 'B'

        elif self.char in OPERARIONS:
            if self.buffer != '':
                self.lexems.append(self.buffer)
            self.lexems.append(self.char)
            self.buffer = ''
            return 'S'
        
        self.raise_exception()

    def state_B(self):
        if self.char == ')':
            self.brackets_count -= 1
            if self.buffer != '':
                self.lexems.append(self.buffer)
            self.lexems.append(self.char)
            self.buffer = ''
            return 'B'

        elif self.char in OPERARIONS:
            if self.buffer != '':
                self.lexems.append(self.buffer)
            self.lexems.append(self.char)
            self.buffer = ''
            return 'S'

        self.raise_exception()

    def state_F(self):
        if self.char.isalpha() and self.char != 'x':
            self.buffer += self.char
            return 'F'

        elif self.char == '(':
            self.brackets_count += 1
            self.lexems.append(self.buffer)
            self.lexems.append(self.char)
            self.buffer = ''
            return 'S'

        self.raise_exception()

    def state_X(self):
        if self.char in OPERARIONS:
            if self.buffer != '':
                self.lexems.append(self.buffer)
            self.lexems.append(self.char)
            self.buffer = ''
            return 'S'

        elif self.char == ')':
            self.brackets_count -= 1
            if self.buffer != '':
                self.lexems.append(self.buffer)
            self.lexems.append(self.char)
            self.buffer = ''
            return 'B'

        self.raise_exception()
    
    def toint(self, e):
        for char in range(len(e)):
            try:
                e[char] = float(e[char])
            except ValueError:
                pass
        return e

    def divide(self, expression : str):
        expression = expression.replace(' ', '')

        if expression[-1] in OPERARIONS:
            self.state = 'O'
            self.char = expression[-1]
            self.raise_exception()

        for _char in expression:
            
            self.char = _char.lower()
            self.state = self.machine[self.state]()

        self.lexems.append(self.buffer)
        
        if self.brackets_count != 0:
            self.char = self.brackets_count
            self.state = 'RB'
            
            self.raise_exception()

        return self.toint(self.lexems)