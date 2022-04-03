from rpn import RPN

class Solver(RPN):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression

    def solve(self, lexems=[]):
        if len(lexems) == 0:
            lexems = self.RPN()
        buffer = []

        if 'x' in lexems:
            return self.equation()

        for lex in lexems:
            if isinstance(lex, float):
                buffer.append(lex)

            elif lex in self.FUNC1:
                buffer.append(self.FUNC1[lex](buffer.pop()))

            else:
                buffer.append(self.FUNC2[lex](buffer.pop(), buffer.pop()))

        return buffer.pop()

    def _replace(self, sub: float):
        buffer = self.lexems.copy()

        for index, lex in enumerate(buffer):
            if lex == 'x':
                buffer[index] = sub

        return buffer

    def equation(self):

        print('Введите интервал')
        start = float(input('От: '))
        end = float(input('До: '))
        FUNC = lambda sub: self.solve(self._replace(sub))

        print('''Варианты повората событий:
        1)Найти корни на промежутке
        2)Найти логарифм
        ''')
        mode = int(input('>')) - 1

        if mode:
            return self.integral(start, end, FUNC)

        else:
            return self.search_root(start, end, FUNC)

    def integral(self, start: int, end: int, f):
        ACCURACY = 10_000
        dx = (end - start) / ACCURACY
        res = 0

        for xi in range(ACCURACY):
            res += (dx / 6) * (f(start + xi * dx) + 4 * f((2 * start + (2 * xi + 1) * dx) / 2) + f(start + (xi + 1) * dx))

        return f'Логарифм: {res}'

    def search_root(self, start: int, end: int, f):
        x = start
        FAULT = 0.00000001
        f = lambda sub: self.solve(self._replace(sub))

        if f(start) * f(end) > 0:
            return 'Невозможно найти корни на данном промежутке...'

        else:
            while f(start) * f(end) < 0 and abs(f(x)) > FAULT:

                k = (f(start) - f(end)) / (start - end)
                b = f(start) - k * start
                x = -b / k

                if f(x) * f(start) > 0:
                    start = x
                else:
                    end = x
                
            return f'Корень выражения: {x}'