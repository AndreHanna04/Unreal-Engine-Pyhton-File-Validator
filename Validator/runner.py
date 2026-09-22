
from .context.context import ValidationContext, AssetMetadata
from typing import Type, NamedTuple
from .config import Config
import argparse
from pathlib import Path
from .registry import registry
from .rules.base import MasterRule, Severity, RuleType, ValidationResult



# Colours
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
RESET = "\033[0m"





class ValidationRunner():


    def __init__(self,
                config: Config,
                 context:ValidationContext | None = None,
                rule_type:RuleType | None = None,
                rule_severity:Severity | None = None,
                rule_list:list[MasterRule] | None = None ,
               ) -> None:
        
        self.config = config
        self.allowlist = config.load_allowlist()
        self.context = context


        if rule_list is not None:
            acceptedlist:list[MasterRule] = [R(config, context) for R in rule_list]

        else:
            registry.discover()
            acceptedlist = [R(config, context) for R in registry.get_rules(category=rule_type, severity=rule_severity)]

        if rule_type is not None:
            filter:list[MasterRule] = []
            for rule in acceptedlist:
                if rule.rule_type is rule_type:
                    filter.append(rule)

            acceptedlist = filter

        if rule_severity is not None:
            filter:list[MasterRule] = []
            for rule in acceptedlist:
                if rule.severity is rule_severity:
                    filter.append(rule)

            acceptedlist = filter

        self.rules = acceptedlist


        

    def validate_asset(self, asset_path:str, rules:list[MasterRule]) -> list[ValidationResult]:
        results :list[ValidationResult] = []
        for rule in rules:
            match = next((e for e in self.allowlist if e.matches(asset_path, rule.rule_name)), None)
            if match is not None:
                results.append(rule.make_skipped(asset_path, f" asset {match.asset} was placed on the allow list by {match.author} under the reason: {match.reason}"))
            else:
                results.append(rule.validate(asset_path))
        return results


 

    def run_validation(self, summary_only:bool = True, asset_paths: list[str] | None = None) -> list[list[ValidationResult]]:
        
        if asset_paths is None:
            if self.context is None:
                print(f" {RED}[Runner] Validation needs either a valid context, or a asset paths{RESET}")
                return []

            asset_paths = [m.path for m in self.context.get_assets()]

        print(f"Scanning {len(asset_paths)} assets")

        all_results: list[list[ValidationResult]] = []

        for path in asset_paths:
            results = self.validate_asset(path, self.rules)
            all_results.append(results)
            for r in results:
                if not summary_only:
                    print(r)
            print()

        return all_results

    