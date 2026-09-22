from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Any
 
@dataclass
class AssetMetadata:
    path: str
    name: str
    extension: str
    size_bytes: int = 0
    asset_class: str = "" # empty in filesystem context
    extra: dict[str, Any] = field(default_factory=dict)
 
class ValidationContext(ABC):

    

    @abstractmethod
    def get_assets(self) -> list[AssetMetadata]: ...
    @abstractmethod
    def get_asset_metadata(self, path: str) -> AssetMetadata | None: ...
  
 
