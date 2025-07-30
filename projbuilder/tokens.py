class Token:
    def __init__(self, children):
        self.children = children
        self.next = None

    def append(self, token: "Token"):
        if type(token) in self.children:
            self.next = token
            return token
        else:
            raise Exception()


class LSquig(Token):
    def __init__(self):
        super().__init__({})


class RSquig(Token):
    pass


class LBrack(Token):
    pass


class RBrack(Token):

    def __init__(self):
        super().__init__({})


class Literal(Token):
    def __init__(self, literal_str: str):
        super().__init__({LSquig})
        self.literal_str = literal_str
    pass


class AssignmentOp(Token):
    pass


class Comma(Token):
    pass


class Root(Token):
    pass

