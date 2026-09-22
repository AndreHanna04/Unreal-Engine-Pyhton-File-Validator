

from typing import Type
from .rules.base import MasterRule






class RuleRegistry():
    
    _instance: "RuleRegistry | None" = None

    def __init__(self) -> None:
        self._rules : dict[str, Type[MasterRule]] = {}

    def __new__(cls) -> "RuleRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._rules = {}
        return cls._instance
    


    def register(self, cls:type[MasterRule]) -> Type[MasterRule]:
        if not cls.rule_name or not cls.rule_type:
            raise ValueError(f" rule class {cls.__name__} has an empty rule name and/or rule type")
        if cls.rule_name in self._rules:
            raise ValueError(f" rule {cls.rule_name} is already registered")
        self._rules[cls.rule_name] = cls
        return cls

    def get_rules(self, category=None, severity=None) -> list[Type[MasterRule]]:
        rules = list(self._rules.values())
        if category: rules = [r for r in rules if r.rule_type == category]
        if severity: rules = [r for r in rules if r.severity is severity]
        return rules

    def get_rule(self, name: str) -> Type[MasterRule] | None:
        return self._rules.get(name)
    
    def discover(self) -> None:

        import importlib, pkgutil
        from . import rules as rules_pkg
        for _, name, _ in pkgutil.iter_modules(rules_pkg.__path__):
            if name != "base":
                importlib.import_module(f".rules.{name}", package=__package__)

registry = RuleRegistry()
            