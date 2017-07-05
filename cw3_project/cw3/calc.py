import inspect
import io
import json
import re
from abc import ABCMeta, abstractmethod
from math import *
from typing import Iterable

import matplotlib.pyplot as plt
from matplotlib import numpy as np

from cw3.CalculationLog import CalculationLog
from cw3.Eq import Eq

NAME_REGEXP = re.compile(r"^[A-Za-z]+[A-Za-z0-9]*$")
PRINT_FUN_REGEXP = re.compile(r"^(print\()[\s\S]*(\))$")
PRINT_FUN_ARGS_REGEXP = re.compile(r"^(print\()(.+?)(\))$")

PLOT_FUN_REGEXP = re.compile(r"^(plot\()[\s\S]*(\))$")
PLOT_FUN_ARGS_REGEXP = re.compile(r"^(plot\()(.+?)(\))$")
stuff = ''


class CodeGenerator(metaclass=ABCMeta):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def check(self, line: str) -> bool:
        """"""

    @abstractmethod
    def to_code(self, line: str, space_offset: str) -> str:
        """"""


class SystemPrintFunctionCheck(CodeGenerator):
    for_insert = ''

    def to_code(self, line: str, space_offset: str) -> str:
        return f'{space_offset}{self.for_insert}'

    def check(self, line: str) -> bool:
        self.for_insert = ''
        if PRINT_FUN_REGEXP.fullmatch(line) is not None:
            self.for_insert = f'self.log_card().add_line({PRINT_FUN_ARGS_REGEXP.search(line).group(2)})'
            return True
        return False


class SystemPlotFunctionCheck(CodeGenerator):
    for_insert = ''

    def to_code(self, line: str, space_offset: str) -> str:
        puts = self.for_insert.split(',')
        return f'{space_offset}def plot() -> str:\n' \
               f'{space_offset}{space_offset}x_rand12as321_x = np.arange({puts[1]},{puts[2]}+{puts[3]}/2,{puts[3]})\n' \
               f'{space_offset}{space_offset}y_randeiru48f48_y = [{puts[0]}(i) for i in x_rand12as321_x]\n' \
               f'{space_offset}{space_offset}\n' \
               f'{space_offset}{space_offset}fig = plt.figure()\n' \
               f'{space_offset}{space_offset}ax = fig.gca()\n' \
               f'{space_offset}{space_offset}step_rand8jrj4_step = ' \
               f'(max(x_rand12as321_x) - min(x_rand12as321_x))/10\n' \
               f'{space_offset}{space_offset}ax.set_xticks(' \
               f'np.arange(min(x_rand12as321_x), ' \
               f'max(x_rand12as321_x)+step_rand8jrj4_step/2, ' \
               f'step_rand8jrj4_step))\n' \
               f'{space_offset}{space_offset}step_rand8jrj4_step = ' \
               f'(max(y_randeiru48f48_y) - min(y_randeiru48f48_y))/10\n' \
               f'{space_offset}{space_offset}ax.set_yticks(' \
               f'np.arange(min(y_randeiru48f48_y), ' \
               f'max(y_randeiru48f48_y) + step_rand8jrj4_step/2, ' \
               f'step_rand8jrj4_step))\n' \
               f'{space_offset}{space_offset}plt.plot(x_rand12as321_x, y_randeiru48f48_y)\n' \
               f'{space_offset}{space_offset}\n' \
               f'{space_offset}{space_offset}plt.grid()\n' \
               f'{space_offset}{space_offset}\n' \
               f'{space_offset}{space_offset}imgdata = io.BytesIO()\n' \
               f'{space_offset}{space_offset}fig.savefig(imgdata, format=\'png\', transparent=True)\n' \
               f'{space_offset}{space_offset}imgdata.seek(0)\n' \
               f'{space_offset}{space_offset}svg_dta = imgdata.getvalue() \n' \
               f'{space_offset}{space_offset}\n' \
               f'{space_offset}{space_offset}plt.close(fig) \n' \
               f'{space_offset}{space_offset}return svg_dta\n' \
               f'{space_offset}\n' \
               f'{space_offset}self.log_card().add_base64_image(plot(),\'image/png\')\n' \
               f'{space_offset}\n' \
               f'{space_offset}\n'

    def check(self, line: str) -> bool:
        self.for_insert = ''
        if PLOT_FUN_REGEXP.fullmatch(line) is not None:
            self.for_insert = f'{PLOT_FUN_ARGS_REGEXP.search(line).group(2)}'
            return True
        return False


class ExpressionCheck(CodeGenerator):
    name = ''
    value = ''

    def to_code(self, line: str, space_offset: str) -> str:
        return f'{space_offset}{self.name} = {self.value}'

    def check(self, line: str) -> bool:
        if '=' not in line:
            return False
        puts = line.split('=')
        if len(puts) != 2:
            return False
        self.name = puts[0].strip()
        self.value = puts[1].strip()
        return True


class UserFunctionCheck(CodeGenerator):
    name = ''
    arguments = []

    def to_code(self, line: str, space_offset: str) -> str:
        return f'\n{space_offset}def {self.name}({", ".join(self.arguments)}):\n' \
               f'{space_offset}    return {line.split("=")[1]}\n'

    def check(self, line: str) -> bool:
        if '=' not in line:
            return False
        if '(' not in line:
            return False
        puts = line.split('(')
        if len(puts) < 2:
            return False
        name = puts[0]
        if NAME_REGEXP.fullmatch(name) is None:
            return False
        self.name = name.strip()
        self.arguments = []

        puts[1] = puts[1].strip()
        if not puts[1].startswith(')'):
            if ',' in puts[1]:
                args = puts[1].split(')')[0]
                args = args.split(',')
                for arg in args:
                    if NAME_REGEXP.fullmatch(arg) is None:
                        return False
                    self.arguments.append(arg)
            else:
                arg = puts[1].split(')')
                if NAME_REGEXP.fullmatch(arg[0]) is None:
                    return False
                self.arguments.append(arg[0])
        return True


class Calculator:
    generators: Iterable[CodeGenerator] = []

    def __init__(self, source_code) -> None:
        super().__init__()
        self.source_code = source_code
        self._init_generators()

        CalculationLog('-1')
        json.dumps({'mock': 'mock'})
        a: plt
        a: io
        a: np
        a: math
        a: Eq

    def _init_generators(self):
        self.generators = [SystemPrintFunctionCheck(),
                           SystemPlotFunctionCheck(),
                           UserFunctionCheck(),
                           ExpressionCheck(), ]

    def generate_code(self):
        logic = self._generate_logic()
        print('logic :: ', logic)
        template = self._get_template_module()
        src = template.replace('###CODE_INSERT###', logic)
        return src

    def execute(self) -> str:
        if 'UserCode' in locals():
            del locals()['UserCode']
        exec(self.generate_code())
        codeObject = locals()['UserCode']()
        result = codeObject.run()
        print(result)
        del codeObject
        return result

    def _get_template_module(self) -> str:
        from cw3 import user_code
        return inspect.getsource(user_code)

    def _generate_logic(self) -> str:
        src = ""
        standard_offset = "        "
        for id, text in self.source_code:
            src += '\n' + standard_offset
            src += "self.create_out_card('" + id + "')"
            lines = text.split('\n')
            for l in lines:
                l = l.strip()
                if len(l) == 0:
                    continue
                found = False
                print("processing string :: ", l)
                for g in self.generators:
                    if g.check(l):
                        found = True
                        src += "\n" + g.to_code(l, standard_offset)
                        break
                if not found:
                    src += f'\n{standard_offset}{l}\n'

        return src
