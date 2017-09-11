import inspect
import re

from numpy import NaN, exp, cos


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
        result = 0
        try:
            x = x - self.start_item
            pos = int(x / self.h)
            if pos < 0 or pos >= self.grid_size:
                return NaN
            x = self.start_item + pos * self.h
            result = self.grid[x]
        except BaseException:
            result = -1
        return result


def one_fun(x):
    return 1.0


def function_hook_with_k(func, k):
    def result(x):
        return k * func(x)

    return result


def function_hook_with_div(func1, func2):
    def result(x):
        return func1(x) * func2(x)

    return result


class Eq(object):
    class Diff(object):
        @staticmethod
        def marginal(source='', a: float = 0, fa: float = 0, b: float = 0, fb: float = 0):
            result = Eq.Diff.EqDiffMarginal(source)
            result.set_condition(a, fa, b, fb)
            return result

        class EqDiffMarginal:
            source: str = ''
            function_name: str = ''
            function_koef = []
            conditions = {}
            split_count = 100

            def __init__(self, source) -> None:
                super().__init__()
                self.source = source.strip()
                self.function_name = self._get_function_name()
                self.function_koef = self._get_function_koef()

            def set_condition(self, a: float, fa: float, b: float, fb: float):
                self.conditions = {'a': a, 'fa': fa, 'b': b, 'fb': fb}

            def _get_function_name(self):
                regex = re.compile(r"([0-9a-zA-Z])[`]+")
                return regex.search(self.source).group(1)

            def _get_function_koef(self):
                puts = re.compile(r"[+|-]").split(self.source)
                puts.sort(key=lambda put: 0 - (put.count('`') * 10 + put.count(self.function_name)))
                puts.remove(puts[0])
                func = [one_fun]
                stack = inspect.stack()
                possibles = globals().copy()
                possibles.update(stack[3].frame.f_locals)  # remove hardcore and paste string code detection
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
                    func.append(function_hook_with_k(method, k))
                return func

            def calculate(self, method='run'):
                if method == 'run':
                    return self.calculate_run_method()
                elif method == 'follow up':
                    return self.calculate_follow_up_method()

            def calculate_run_method(self):
                h = (self.conditions['b'] - self.conditions['a']) / self.split_count
                x0 = self.conditions['a']
                koef = []
                klength = self.split_count - 1
                for i in range(klength):
                    yi = 1.0 / (h ** 2) + self.function_koef[2](x0)
                    yi1 = (-2.0) / (h ** 2) + self.function_koef[1](x0) / h
                    yi2 = 1.0 / (h ** 2) - self.function_koef[1](x0) / h
                    r = self.function_koef[3](x0)
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
                result.name = self.function_name
                result.grid = grid
                result.start_item = self.conditions['a']
                result.h = h
                return result

            def calculate_follow_up_method(self):
                new_fanc_k = []
                for i in range(1, len(self.function_koef)):
                    k = 1 if i == len(self.function_koef)-1 else -1
                    new_fanc_k.append(function_hook_with_k(
                        function_hook_with_div(self.function_koef[i], self.function_koef[0]), k))

                h = (self.conditions['b'] - self.conditions['a']) / self.split_count
                klength = self.split_count

                x = self.conditions['a']
                y = self.conditions['fa']
                dy = 1.5
                grid = {x: y}
                for i in range(klength):
                    dy += h * (new_fanc_k[0](x) * dy + new_fanc_k[1](x) * y + new_fanc_k[2](x))
                    y += h * dy
                    grid[h * i] = y
                    x += h
                grid[self.conditions['b']]=self.conditions['fb']
                grid[self.conditions['a']]=self.conditions['fa']
                result = Function1Arg()
                result.name = self.function_name
                result.grid = grid
                result.start_item = self.conditions['a']
                result.h = h
                return result
