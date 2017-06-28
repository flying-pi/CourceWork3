import json
from typing import Iterable

from cw3.CalculationLog import CalculationLog


class UserCode:
    log_list: Iterable[CalculationLog] = []
    current_code_card = 0

    def __init__(self) -> None:
        super().__init__()

    def clear_log(self):
        self.log_list = []
        self.log_list.append(CalculationLog('-1'))
        self.current_code_card = 0

    def create_out_card(self, put_id: str):
        self.log_list.append(CalculationLog(put_id))
        self.current_code_card += 1

    def log_card(self) -> CalculationLog:
        return self.log_list[self.current_code_card]

    def run(self):
        self.clear_log()
        print("begin execute user code")
        ###CODE_INSERT###
        print("finish execute user code")
        return {'out': [i.to_dictionary() for i in self.log_list if i.put_id != -1]}

