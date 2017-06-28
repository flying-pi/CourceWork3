import inspect
import json
import re
from abc import ABCMeta, abstractmethod
from typing import Iterable

from cw3.CalculationLog import CalculationLog

NAME_REGEXP = re.compile(r"^[A-Za-z]+[A-Za-z0-9]*$")
PRINT_FUN_REGEXP = re.compile(r"^(print\()[\s\S]*(\))$")
PRINT_FUN_ARGS_REGEXP = re.compile(r"^(print\()(.+?)(\))$")

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


class SystemFunctionCheck(CodeGenerator):
    for_insert = ''

    def to_code(self, line: str, space_offset: str) -> str:
        return f'{space_offset}{self.for_insert}'

    def check(self, line: str) -> bool:
        self.for_insert = ''
        if PRINT_FUN_REGEXP.fullmatch(line) is not None:
            self.for_insert = f'self.log_card().add_line({PRINT_FUN_ARGS_REGEXP.search(line).group(2)})'
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
                if NAME_REGEXP.fullmatch(arg) is None:
                    return False
                self.arguments.append(arg)
        return True


class Calculator:
    generators: Iterable[CodeGenerator] = []

    def __init__(self, source_code) -> None:
        super().__init__()
        self.source_code = source_code
        self._init_generators()

        CalculationLog('-1')
        json.dumps({'mock': 'mock'})

    def _init_generators(self):
        self.generators = [SystemFunctionCheck(),
                           UserFunctionCheck(),
                           ExpressionCheck(), ]

    def generate_code(self):
        logic = self._generate_logic()
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
                for g in self.generators:
                    if g.check(l):
                        found = True
                        src += "\n" + g.to_code(l, standard_offset)
                        break

        return src
