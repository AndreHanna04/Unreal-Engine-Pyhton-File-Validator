
import os
from .base import MasterRule, ValidationResult, Severity, RuleType
from ..registry import registry
from ..context.context import AssetMetadata


@registry.register
class ExtentionRule(MasterRule):

    rule_name = "extention_rule"
    rule_type = RuleType.NAMING
    severity = Severity.ERROR

    def validate(self, asset_path):
        if self.context is None:
            return self.make_skipped(asset_path, "No valid context available")
        meta = self.context.get_asset_metadata(asset_path)
        if meta is None:
            _, ext = os.path.splitext(asset_path)
            ext = ext.lower()
        else:
            ext = (meta.extension or '').lower()
        valid = self.config.get("valid_extensions", [])
        if ext in valid:
            return self.make_result(asset_path, True, f"Extension {ext} is allowed")
        return self.make_result(asset_path, False, f"Extension {ext} is not allowed")

@registry.register    
class FileSizeRule(MasterRule):
    rule_name = "filesize_rule"
    rule_type = RuleType.FILESIZE
    severity = Severity.WARNING

    def validate(self, asset_path: str) -> ValidationResult:
        if self.context is None:
            return self.make_skipped(asset_path, "No valid context available")

        meta = self.context.get_asset_metadata(asset_path)
        if meta is None:
            return self.make_result(asset_path, False, "File is the boogeyman - it doesn't exist")

        max_mb = self.config.get("max_file_size_mb", 50)
        file_size = meta.size_bytes / (1024*1024)

        if file_size < max_mb:
            return self.make_result(asset_path, True, f"asset is valid size, less than {max_mb} limit")
        return self.make_result(asset_path, False, f"asset is {file_size}mb which is larger than maximum size of {max_mb} mb")
