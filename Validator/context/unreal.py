from .context import ValidationContext, AssetMetadata
from ..env import UNREAL_AVAILABLE
from typing import Any
import os

if UNREAL_AVAILABLE:
    import unreal

class UnrealContext(ValidationContext):
    def __init__(self, asset_path: str = "/Game/") -> None:
        if not UNREAL_AVAILABLE:
            raise ImportError(
                "UnrealContext requires Unreal Editor. "
                "Use FilesystemContext for standalone Python mode."
            ) # fail at construction - not silently mid-validation
        self.asset_path = asset_path
 
    def get_assets(self) -> list[AssetMetadata]:
        paths = unreal.EditorAssetLibrary.list_assets(self.asset_path, recursive=True)
        return [m for p in paths if (m := self.get_asset_metadata(p))]
    
    def get_asset_metadata(self, path: str) -> AssetMetadata | None:
        try:
           data = unreal.EditorAssetLibrary.find_asset_data(path)
        except Exception:
            return None
        
        if not data.is_valid():
            return None
        
        return AssetMetadata(
             path,
             data.asset_name,
            ".uasset",
            self._get_disk_size_bytes(path),
            str(data.asset_class_path.asset_name ),

               )

    def _get_disk_size_bytes(self, path: str) -> int:
        try:
            obj = unreal.load_asset(path)
            if obj is None:
                return 0
            disk_path = unreal.SystemLibrary.get_system_path(obj)
            if not disk_path or not os.path.isfile(disk_path):
                return 0
            return os.path.getsize(disk_path)
        except Exception:
            return 0

    def load_uobject(self, path:str) -> Any:

        try:
           return unreal.EditorAssetLibrary.load_asset(path)
        except Exception:
            return None