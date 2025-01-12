import typing

# redo the Signal class with type annotations
# types of parameters of emit method are specify with creation of Signal class
class Signal[*ArgsT = typing.Unpack[typing.Tuple[()]]]:
    def __init__(self):
        self.handlers: typing.List[typing.Callable[[*ArgsT], None]] = []

    def connect(self, handler: typing.Callable[[*ArgsT], None]):
        self.handlers.append(handler)

    def disconnect(self, handler: typing.Callable[[*ArgsT], None]):
        self.handlers.remove(handler)

    def emit(self, *args: *ArgsT):
        for handler in self.handlers:
            handler(*args)
