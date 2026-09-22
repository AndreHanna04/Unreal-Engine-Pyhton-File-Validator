
from datetime import date, datetime
import fnmatch
from dataclasses import dataclass


@dataclass
class AllowListEntry:
    rule_name:str
    asset:str
    reason: str
    author: str
    expiry: str |None = None


    def _is_expired(self) -> bool:
        if self.expiry is None:
            return False
        return date.today() > datetime.strptime(self.expiry, "%Y-%m-%d").date()

    #written to check allows before rule is evaluated to save execution time
    def matches(self, asset:str, rule_name:str) -> bool:
        if self._is_expired():
            return False
        if rule_name != self.rule_name:
            return False

        normalized_asset = asset.replace("\\", "/")
        normalized_pattern = self.asset.replace("\\", "/")
        return fnmatch.fnmatch(normalized_asset, normalized_pattern)
