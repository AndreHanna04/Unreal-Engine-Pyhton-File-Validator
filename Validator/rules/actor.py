
import os
from .base import MasterRule, ValidationResult, Severity, RuleType
from ..registry import registry
from ..env import UNREAL_AVAILABLE


@registry.register
class Tickrule(MasterRule):

    rule_name = "tick_rule"
    rule_type = RuleType.ACTOR
    severity = Severity.ERROR

    def validate(self, asset_path):
       
       if not UNREAL_AVAILABLE:
        return self.make_skipped(asset_path, f"Unreal Environment is unavailable: Skipping asset")
       
       import unreal

       asset = unreal.load_asset(asset_path)

       if not isinstance(asset, unreal.Blueprint):
        return self.make_skipped(asset_path, f"Rule is only applicable to Blueprints, asset isn't a Blueprint")

       generated_class = asset.generated_class()
       if generated_class is None:
        return self.make_skipped(asset_path, f"Blueprint has no generated class (not compiled?)")

       cdo = unreal.get_default_object(generated_class)
       if not isinstance(cdo, unreal.Actor):
        return self.make_skipped(asset_path, f"Rule is only applicable to actors, asset isn't a child of Actor")

       cantick:bool = cdo.get_editor_property("primary_actor_tick").get_editor_property("start_with_tick_enabled")
       tag_name:str = self.config.get("actor_tick_tag", "tick")
       has_tag:bool = bool(unreal.EditorAssetLibrary.get_metadata_tag(asset, tag_name))

       if cantick and not has_tag:
           return self.make_result(asset_path, False, f"Actor has tick enabled but is missing the required '{tag_name}' tag")
       return self.make_result(asset_path, True, f"Tick/tag check passed")
