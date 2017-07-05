import inspect
import re

from numpy import NaN


class Function1Arg:
    expression = 'x+2'
    name = 'f'
    _grid = []
    start_item = 0
    h = 1
    grid_size = 0

    def __init__(self) -> None:
        super().__init__()

    def get_source(self, space_offset: str):
        return f'{space_offset}def {self.name}(x):\n' \
               f'{space_offset}{space_offset}return {self.expression}'

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, value):
        self._grid = value
        self.grid_size = len(value)

    def __call__(self, x):
        x = x - self.start_item
        pos = int(x / self.h)
        if pos < 0 or pos >= self.grid_size:
            return NaN
        x = self.start_item+pos*self.h
        result = self.grid[x];
        return result


def one_fun(x):
    return 1


def function_hook(func, k):
    def result(x):
        return k * func(x)

    return result


class Eq(object):
    class Diff(object):
        @staticmethod
        def marginal(source='', a: float = 0, fa: float = 0, b: float = 0, fb: float = 0):
            result = Eq.Diff.EqDiffMarginal()
            result.source = source
            result.set_condition(a, fa, b, fb)
            return result

        class EqDiffMarginal:
            source: str = ''
            conditions = {}

            def __init__(self) -> None:
                super().__init__()

            def set_condition(self, a: float, fa: float, b: float, fb: float):
                self.conditions = {'a': a, 'fa': fa, 'b': b, 'fb': fb}

            def calculate(self):
                self.source = self.source.strip()
                regex = re.compile(r"([0-9a-zA-Z])[`]+")
                function_name = regex.search(self.source).group(1)
                puts = re.compile(r"[+|-]").split(self.source)
                puts.sort(key=lambda put: 0 - (put.count('`') * 10 + put.count(function_name)))
                puts.remove(puts[0])
                print(function_name)
                func = [one_fun]
                stack = inspect.stack()
                possibles = globals().copy()
                possibles.update(stack[1].frame.f_locals)
                fun_name_regexp = re.compile(r"(\S)\(\S\)")
                for i in range(len(puts)):
                    method_name = fun_name_regexp.search(puts[i]).group(1)
                    method = possibles.get(method_name)
                    if method is None:
                        method = lambda x: 1
                        print("can not found method by name :: ", method_name, "\ttesting :: ", method(12))
                    k = -1 if self.source.split(puts[i])[0].strip()[-1] == '-' else 1
                    if i == (len(puts) - 1):
                        k *= -1
                    func.append(function_hook(method, k))
                split_count = 100
                h = (self.conditions['b'] - self.conditions['a']) / split_count
                x0 = self.conditions['a']
                koef = []
                klength = split_count - 1
                for i in range(klength):
                    yi = 1.0 / (h ** 2) + func[2](x0)
                    yi1 = (-2.0) / (h ** 2) + func[1](x0) / h
                    yi2 = 1.0 / (h ** 2) - func[1](x0) / h
                    r = func[3](x0)
                    koef.append([yi, yi1, yi2, r])
                    x0 += h

                koef[0][3] -= koef[0][0] * self.conditions['fa']
                koef[0][0] = 0

                koef[klength - 1][3] -= koef[klength - 1][2] * self.conditions['fb']
                koef[klength - 1][2] = 0

                for i in range(klength - 1):
                    k = koef[i + 1][0] / koef[i][1]
                    koef[i + 1][0] -= (koef[i][1] * k)
                    koef[i + 1][1] -= (koef[i][2] * k)
                    koef[i + 1][3] -= (koef[i][3] * k)

                for i in range(klength - 1, -1, -1):
                    k = koef[i - 1][2] / koef[i][1]
                    koef[i - 1][2] -= (koef[i][1] * k)
                    koef[i - 1][3] -= (koef[i][3] * k)
                grid = {self.conditions['a'] + h * (i + 1): koef[i][3] / koef[i][1] for i in range(klength)}

                grid[self.conditions['a']] = self.conditions['fa']
                grid[self.conditions['b']] = self.conditions['fb']

                result = Function1Arg()
                result.name = function_name
                result.grid = grid
                result.start_item = self.conditions['a']
                result.h = h
                return result
