
from .Validator.env import UNREAL_AVAILABLE

if UNREAL_AVAILABLE:
    import unreal

    @unreal.uclass()
    class ValidatorSettings(unreal.DeveloperSettings):
        max_file_size_mb = unreal.uproperty(int, meta=dict(Category="Validator"))
        max_filename_length = unreal.uproperty(int, meta=dict(Category="Validator"))
        naming_pattern = unreal.uproperty(str, meta=dict(Category="Validator"))
        valid_extensions = unreal.uproperty(unreal.Array(str), meta=dict(Category="Validator"))
        actor_tick_tag = unreal.uproperty(str, meta=dict(Category="Validator"))

        def _post_init(self):
            self.max_file_size_mb = 50
            self.max_filename_length = 64
            self.naming_pattern = r"^[A-Z][a-zA-Z0-9_]+$"
            self.valid_extensions = [".png", ".uasset", ".exr", ".tga", ".fbx"]
            self.actor_tick_tag = "tick"
else:
    ValidatorSettings = None
