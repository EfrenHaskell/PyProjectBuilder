import objects as obj

"""
Production -> sequence of expansions or productions
Expansions -> set of tokens of a specific token type
Literal -> any generic token
"""


class Expansion:
    def __init__(self, optional: bool):
        self.expansions: dict[str: Production] = {}
        self.optional = optional
        self.value = None

    def match(self, token: str) -> (bool, "Production"):
        if token in self.expansions:
            self.value = self.expansions[token]
            return True
        else:
            return False


class Literal:
    def __init__(self, optional: bool = False):
        self.optional = optional

    @staticmethod
    def match():
        return True


class Production:
    def __init__(self, sequence, output_obj):
        self.sequence: list[Expansion | Literal] = sequence
        self.output_obj = output_obj

    def follow(self, line_tokens: list[str]):
        for index, token in enumerate(line_tokens):
            self.sequence[index].match(token)

    def get_obj(self):
        return self.output_obj


class DirProduction(Production):
    def __init__(self):
        super().__init__([Literal(optional=True)], obj.DirObj())


class FileProduction(Production):
    def __init__(self):
        super().__init__([Literal()], obj.FileObj())

