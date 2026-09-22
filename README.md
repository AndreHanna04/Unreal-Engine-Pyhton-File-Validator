# Validator

A simple validator that by default scans the files in it's current parent directory and checks if the files pass certain rules

## Implemented Rules
The current implemented rules are as follows:
- Extension rule - Checks if a file's extension matches one on the allowed list
- Filesize rule - Checks if a file's size is smaller than the required amount (50mb)
- Actor Tick Rule - Checks if an actor has the required tick tag(this is configurable through the config file under "actor_tick_tag")
  - This rule exists to prevent actors ticking unnecessarily. Over a large number of actors, this can greatly impact performance
- Material double sided rule - Checks if an material has the double sided property enabled. 
  - Most materials usually don't need this and disabling it halves the performance cost of the material.

## Arguements
- --directory [Directory] : provide a custom directory for the validator to scan
- --summary_only : will not display each individual pass and fail and instead only show a short summary
- --config [Config Path] : provide a custom JSON config file (see `config.json` in the project root for a working example)
- --rule_type [RULE_TYPE] : only run rules belonging to one category (NAMING, FILESIZE, ACTOR, MATERIAL, MISC, IMAGES)
- --rule_severity [SEVERITY] : only run rules of a given severity (ERROR, WARNING, INFO)
- --rule_list [rule_name,rule_name,...] : only run specific rules by name, e.g. `extention_rule,filesize_rule`
- --log [File Path] : write a structured JSON report of the results to the given path (see Structured Output below)

Example: `python runstep.py --directory ./Content --rule_type NAMING --log reports/sample_output.json`

## Allowlist
Individual (asset, rule) combinations can be exempted from validation by adding entries under the `allowlist` key in your config file. A matching entry causes that rule to be skipped for that asset instead of run, and the skip message records who added it and why.

```json
"allowlist": [
  {
    "rule_name": "filesize_rule",
    "asset": "*/Cutscenes/*.uasset",
    "reason": "Pending compression pass, ticket VAL-42",
    "author": "andre",
    "expiry": "2026-09-01"
  }
]
```
- `rule_name` : must exactly match the rule's `rule_name` (e.g. `extention_rule`)
- `asset` : a glob pattern matched against the asset path. Both `/` and `\` are normalized before matching, so the same pattern works against Windows filesystem paths and Unreal `/Game/...` paths
- `reason` / `author` : recorded and shown in the skip message
- `expiry` : optional `YYYY-MM-DD` date. Once passed, the entry stops applying and the rule runs normally again

## Structured Output
Pass `--log [File Path]` to write a structured JSON report alongside the normal console/Output Log output. It contains a summary block plus a per-asset breakdown of every rule that ran:

```json
{
  "generated_at": "2026-07-28 23:27",
  "summary": {
    "asset_pass_count": 1,
    "rule_pass_count": 7,
    "asset_fail_count": 1,
    "rule_fail_count": 1,
    "rule_skip_count": 4
  },
  "assets": [
    {
      "asset_path": "SM_TestMesh.fbx",
      "checks": [
        {
          "rule_name": "extention_rule",
          "rule_category": "NAMING",
          "rule_severity": "ERROR",
          "passed": true,
          "skipped": false,
          "message": "Extension .fbx is allowed"
        }
      ]
    }
  ]
}
```
The `generated_at` field is stamped with the date and time (to the minute) the report was written. A plain-text pass/fail summary always prints to the console/Output Log regardless of whether `--log` is used.

## Extending rules
To add a rule, you can either duplicate the rule_template.py inside of rules folder, or create a python file in the rules folder that contains your rule class. Your python file must:
- import these modules:
```
from .base import MasterRule, ValidationResult, Severity, RuleType
from ..registry import registry
```
- rule class must subclass from MasterRule
- rule class must have a valid rule_name, rule_type and severity
```
    rule_name = "..."
    rule_type = RuleType.NAMING
    severity = Severity.ERROR
```
- implement a validate function
```
def validate(self, asset_path:str) -> ValidationResult:
 
```
- rule class must be decorated with:

```
@registry.register
```

## Unreal Rules

For a rule to integrate into the unreal framework, it must have:

```
from .env import UNREAL_AVAILABLE
```

and within it's validate function, it must check if UNREAL_AVAILABLE is true before importing the unreal module which would look like this:

```
 def validate(self, asset_path: str) -> ValidationResult:
        if not UNREAL_AVAILABLE:
            return self.make_skipped(asset_path, "Unreal Engine not available.")
        import unreal
```

## Connecting to Unreal

1. Add this repo's root folder (the one containing `Validator/`) to Unreal's Python path: **Edit → Project Settings → Plugins → Python → Additional Paths**.
2. Make sure the Python Editor Script Plugin is enabled: **Edit → Plugins → search "Python"**.
3. In your Unreal project, create `Content/Python/init_unreal.py` (if it doesn't already exist) containing:
```
import Validator.unreal_startup_script
```
This file runs automatically every time the Editor starts, and registers the "Validate Assets" context menu entry.

## Validating Inside Unreal

- Right-click a folder in the Content Browser's folder tree and select **Validate Assets**.
- Results and a pass/fail summary print to the Output Log, prefixed `[Validator]`.
- Validating from the menu automatically writes a structured JSON log to the Unreal project's root folder — no `--log` flag needed, this happens on every run. The filename includes the date and time the report was generated, down to the minute, e.g. `validation_report_2026-07-28_23-27.json`. If multiple folders are selected at once, each folder is validated in turn and the file is overwritten with the most recently processed folder's results (all within the same run share one filename/timestamp).
- Unreal-specific rules (Actor Tick Rule, Material double sided rule) only run when the Unreal Editor's Python environment is available — outside Unreal they're skipped automatically.