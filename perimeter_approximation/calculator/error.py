from dataclasses import dataclass, field

class CalculatorError(Exception):
    pass

@dataclass
class OperatorError(Exception):
    failed_index: int = field(init=False)
