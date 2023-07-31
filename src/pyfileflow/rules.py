from enum import Enum, unique
from .utils.types import SupportedPathTypes, PathListType

@unique
class RuleType(str, Enum):
    move = "move"
    copy = "copy"
    #log = "log"

class Rule:
    pass
    #def __init__(self, rule_type : RuleType = "move", target_directory : SupportedPathTypes):

