class Funcs:

    def __init__(self):
        self.func_map = FuncMap({
            1: self.func1,
            2: self.func2
        })

    def map(self, inp: int):
        self.func_map.exec(inp)

    @staticmethod
    def func1():
        print("function 1")

    @staticmethod
    def func2():
        print("function 2")


class FuncMap:

    def __init__(self, funcs):
        self.funcs = funcs

    def exec(self, inp: int):
        self.funcs[inp]()
