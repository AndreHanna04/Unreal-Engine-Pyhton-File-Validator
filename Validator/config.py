
import json
from typing import Any
from pathlib import Path
from.allowlist import AllowListEntry
import os

DEFAULT:dict[str, Any] = {
    "max_file_size_mb" : 50,
    "max_filename_length": 64,
    "naming_pattern" : r"^[A-Z][a-zA-Z0-9_]+$",
    "required_prefixes": {
        "SM_": [".fbx", ".uasset", ".gltf"],
        "T_": [".png", ".exr", ".tga"],
        "M_": [".uasset"],
        },
    "valid_extensions" : [".png", ".uasset", ".exr", ".tga", ".fbx"],
    "actor_tick_tag" : "tick",
    "allowlist" : [],

}

class Config:
  def __init__(self, config_path:str | None = None ) -> None:
    self._data: dict[str, Any] = dict(DEFAULT)
    self.load_json(config_path or os.environ.get("VALIDATOR_CONFIG_PATH"))
    self._load_env()

  def load_json(self, config_path:str | None) -> None:
    if config_path is None:
      return
    try:
      with open(config_path, "r", encoding="utf-8") as fh:
        overrides = json.load(fh)
      if not isinstance(overrides, dict):
        raise ValueError(f" Config file must be object of type dict but is instead {type(overrides).__name__}")
      self._data.update(overrides)
      print(f"config file loaded from {config_path}")
    except FileNotFoundError:
      print(f" config file not found at {config_path}")
    except (json.JSONDecodeError, ValueError) as exc:
      print(f"unable to parse {config_path} - {exc}")
    

  def _load_env(self) -> None:
    prefix = "VALIDATOR_"
    for env_key, raw_value in os.environ.items():
      if not env_key.startswith(prefix):
        continue
      key = env_key[len(prefix):].lower()
      if key == "config_path":
        continue
      self._data[key] = self._coerce(key,raw_value)


  def load_allowlist(self) -> list[AllowListEntry]:
      return [AllowListEntry(**entry) for entry in self._data.get("allowlist", [])]

  def _coerce(self, key:str, raw:str) -> Any:
    if key not in DEFAULT:
      return raw
    default = DEFAULT[key]
    try:
      if isinstance(default, bool):
        return raw.strip().lower() in ["1", "true", "yes", "on"]
      if isinstance(default, int):
        return int(raw)
      if isinstance(default, float):
        return float(raw)
      if isinstance(default, (list, dict)):
        return json.loads(raw)
    except (json.JSONDecodeError, ValueError) as exc:
      print(f" could not coerse  {key} = {raw} : {exc}")
    return raw


  def get(self, key:str, default: Any = None) -> Any:
    return self._data.get(key, default)
  
  def __getitem__(self, key):
    return self._data[key]
  
  def __contains__(self, item):
    return item in self._data
  
  def __repr__(self) -> str:
    return f" Config({self._data!r})"
    



    
     
