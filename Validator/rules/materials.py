import os
from .base import MasterRule, ValidationResult, Severity, RuleType
from ..env import UNREAL_AVAILABLE
from ..registry import registry


@registry.register
class MaterialTwoSidedRule(MasterRule):
    rule_name = "material_two_sided"
    rule_type = RuleType.MATERIAL
    severity = Severity.WARNING
    def validate(self, asset_path: str) -> ValidationResult:
        if not UNREAL_AVAILABLE:
            return self.make_skipped(asset_path, "Unreal Engine not available.")
        import unreal

        mat = unreal.EditorAssetLibrary.load_asset(asset_path)
        if mat is None or not isinstance(mat, unreal.Material):
            return self.make_skipped(asset_path, "Asset is not a Material.")
        if mat.get_editor_property("two_sided"):
            return self.make_result(asset_path, False,
    "two_sided=True doubles rasterisation cost. "
    "Disable unless front and back of each geometry face will be visible")
        return self.make_result(asset_path, True, "Single-sided - culling applies.")