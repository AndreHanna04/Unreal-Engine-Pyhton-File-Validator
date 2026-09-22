

from typing import TYPE_CHECKING

try:
    import unreal
    UNREAL_VERSION: str | None = unreal.SystemLibrary.get_engine_version()[:5]
    UNREAL_AVAILABLE: bool = True
except Exception:
    unreal = None
    UNREAL_VERSION: str | None = None
    UNREAL_AVAILABLE: bool = False

if TYPE_CHECKING:
    import unreal


ASSET_CLASS_STATIC_MESH = "StaticMesh"
ASSET_CLASS_MATERIAL = "Material"
ASSET_CLASS_TEXTURE2D = "Texture2D"
ASSET_CLASS_SKELETON = "Skeleton"
ASSET_CLASS_NIAGRA = "NiagraSystem"
ASSET_CLASS_ANIM = "AnimSequence"



def get_content_path() -> str | None:
    if UNREAL_AVAILABLE:
        return unreal.Paths.project_content_dir()
    return None
    
def get_project_path() -> str | None:
    if UNREAL_AVAILABLE:
        return unreal.Paths.project_dir()
    return None
    
def get_selected_assets() -> list:
    if UNREAL_AVAILABLE:
        return unreal.EditorUtilityLibrary.get_selected_assets()
    return []

