import base64
from abc import ABCMeta, abstractmethod
from typing import Dict


class LogItem(metaclass=ABCMeta):
    @abstractmethod
    def type(self) -> str:
        """"""

    @abstractmethod
    def data(self):
        """"""

    def to_dictionary(self, pos: int = 0) -> Dict:
        return {'type': self.type(), 'data': self.data(), 'order': pos}


class TextLogItem(LogItem):
    text: str = ''

    def type(self) -> str:
        return 'text'

    def data(self):
        return self.text

    def __init__(self, message) -> None:
        super().__init__()
        for m in message:
            self.text += str(m) + '\t'
        self.text = self.text.strip()


class Base64ImageLogItem(LogItem):
    b64image: str = ''

    def type(self) -> str:
        return 'base64'

    def data(self):
        return self.b64image

    def __init__(self, raw, t) -> None:
        super().__init__()
        b64 = base64.b64encode(raw)
        self.b64image = 'data:' + t + ';base64,' + str(b64, 'utf-8')


class CalculationLog:
    items = []

    def __init__(self, put_id) -> None:
        super().__init__()
        self.put_id = put_id
        self.items = []

    def add_line(self, *arg):
        self.items.append(TextLogItem(arg))

    def add_base64_image(self, b64, t):
        self.items.append(Base64ImageLogItem(b64, t))

    def to_dictionary(self):
        return {'put_id': int(self.put_id),
                'items': [self.items[i].to_dictionary(i) for i in range(len(self.items))]}
