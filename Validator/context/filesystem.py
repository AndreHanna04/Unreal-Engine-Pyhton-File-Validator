import os
from typing import Any
from .context import AssetMetadata, ValidationContext


class FileSystemcontext(ValidationContext):

    def __init__(self, directory:str) -> None:
        if not os.path.isdir(directory):
            raise ValueError(f"Filesystem context : {directory} is invalid")
        
        self.directory = os.path.abspath(directory)

    def get_asset_metadata(self, path: str) -> AssetMetadata | None:

        if not os.path.isfile(path):
            return None

        name = os.path.splitext(os.path.basename(path))[0]
        _, ext = os.path.splitext(path)
        extension = ext.lower()
    

        try:
            size_bytes = os.path.getsize(path)
        except OSError:
            size_bytes = 0

        return AssetMetadata(path, name, extension, size_bytes, "", {} )
    
    def get_assets(self) -> list[AssetMetadata]:

        assets:list[AssetMetadata] = []
        for root, _dirs, files in os.walk(self.directory):
            for filename in sorted(files):
                full_path = os.path.join(root, filename)
                meta = self.get_asset_metadata(full_path)
                if meta is not None:
                    assets.append(meta)
        
        return assets

        