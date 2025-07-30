from enum import Enum


class Err(Enum):
    TokenLength = "Parse error: exceeds token length for expected expression"
    ContextSpec = "Parse error: no context specified"
    EnterError = "Parse error: attempted to enter into non-enterable or non-existent element"
    NestError = "Parse error: context can not be nested"
    ContextOrderMismatch = "Load error: execution order does not match number of contexts"
