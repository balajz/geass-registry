from enum import Enum


class Kind(str, Enum):
    unknown = "unknown"
    template = "template"
    starter = "starter"
    boilerplate = "boilerplate"
