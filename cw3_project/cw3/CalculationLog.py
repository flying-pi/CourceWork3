from abc import ABCMeta, abstractmethod


class LogItem(metaclass=ABCMeta):
    @abstractmethod
    def type(self) -> str:
        """"""

    @abstractmethod
    def data(self):
        """"""

    def to_dictionary(self):
        return {'type': self.type(), 'data': self.data()}


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


class CalculationLog:
    items = []

    def __init__(self, put_id) -> None:
        super().__init__()
        self.put_id = put_id
        self.items = []

    def add_line(self, *arg):
        self.items.append(TextLogItem(arg))

    def to_dictionary(self):
        return {'put_id': int(self.put_id), 'items': [i.to_dictionary() for i in self.items]}
