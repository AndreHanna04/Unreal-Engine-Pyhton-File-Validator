
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from ..context.context import ValidationContext
from pathlib import Path




# Colours
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
RESET = "\033[0m"


class Severity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class RuleType(Enum):
    MISC = "MISC"
    NAMING = "NAMING"
    FILESIZE = "FILESIZE"
    IMAGES = "IMAGES"
    ACTOR = "ACTOR"
    MATERIAL = "MATERIAL"



@dataclass
class ValidationResult():
    
    asset_path : str
    category: RuleType
    validation_pass : bool
    severity : Severity
    rule_name :str
    message:str
    skipped: bool = False

    def __str__(self) -> str:
        status = "[PASS]" if self.validation_pass else f"[FAIL][{self.severity.value}]"
        status = "[SKIP]" if self.skipped else status
        rule_col = self.rule_name
        filename = Path(self.asset_path).name
        line = f"[{status}] {rule_col} - {filename}"

        if self.skipped:
            line += f"   -  {self.message}"
        elif not self.validation_pass:
            line += f"   -  {self.message}"
            if self.severity == Severity.ERROR:
                line = f"{RED}{line}{RESET}"
            elif self.severity == Severity.WARNING:
                line = f"{YELLOW}{line}{RESET}"
        else:
            line = f"{GREEN}{line}{RESET}"


        return line



class MasterRule(ABC):

    rule_name : str
    rule_type : RuleType
    severity: Severity


    def __init__(self, config:dict, context:ValidationContext | None = None) -> None:
        self.config = config
        self.context = context


    @abstractmethod
    def validate(self, asset_path:str) -> ValidationResult:
        ...


    def make_result(self, asset_path:str, passed:bool, message:str) -> ValidationResult:
        return ValidationResult(asset_path, self.rule_type,passed, self.severity, self.rule_name, message )
    

    def make_skipped(self, asset_path:str, message:str) -> ValidationResult:
        return ValidationResult(asset_path, self.rule_type, True, Severity.INFO, self.rule_name, message, True)