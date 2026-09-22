
from .runner import ValidationResult
from typing import Type, NamedTuple
from datetime import datetime
import json

class Reporter:

    class Result(NamedTuple):
            #an asset is considered failed if it fails a single rule and considered passed if it passes or skips all applied rules
            asset_pass_count: int
            rule_pass_count:int
            asset_fail_count: int
            rule_fail_count:int
            rule_skip_count: int
     

    def count(self, results:list[list[ValidationResult]], failed_asset_list:list[list[ValidationResult]] | None = None) -> Result:
        asset_passes:int = 0
        asset_failures:int = 0
        rule_skips:int = 0
        rule_passes:int = 0
        rule_fails:int = 0
        failed_assets:list[list[ValidationResult]] = []
        for result in results:
            fail_bool:bool = False
            for subresult in result:
                if not subresult.validation_pass:
                    fail_bool = True
                    rule_fails += 1
                else:
                    rule_passes += 1
                if subresult.skipped:
                    rule_skips += 1

            if fail_bool:
                asset_failures += 1
                failed_assets.append(result)
            else:
                asset_passes += 1

        if failed_asset_list is not None:
            for asset in failed_assets:
                failed_asset_list.append(asset)

        return self.Result(asset_passes, rule_passes, asset_failures, rule_fails, rule_skips)

    
    def print_summary(self, results:list[list[ValidationResult]]) -> None:
            print("SUMMARY \n")
    
            failed_asset_list:list[list[ValidationResult]] = []
            counts = self.count(results, failed_asset_list)
                
    
            
            # add root folder
            print(f" {len(results)} assets scanned")
            print(f" Passed assets: {counts.asset_pass_count}" )
            print(f" Passed rules: {counts.rule_pass_count}" )
            print (f" failed assets : {counts.asset_fail_count}")
            print (f" failed rules: {counts.rule_fail_count}")
            print (f" Skipped Rules : {counts.rule_skip_count}")
    
            print("--- Failed Asset Summary ---")
    
            for asset in failed_asset_list:
                print(f"{asset[0].asset_path} failed checks: ")
                for asset_check in asset:
                    if not asset_check.validation_pass:
                        print(f" {asset_check.rule_name} \n")

    def _result_to_dict(self, result:ValidationResult) -> dict:
        return {
            "rule_name" : result.rule_name,
            "rule_category" : result.category.value,
            "rule_severity" : result.severity.value,
            "passed" : result.validation_pass,
            "message" : result.message,
            "skipped" : result.skipped
        }

    def export_results_json(self, results: list[list[ValidationResult]], output_path: str) -> None:
        counts = self.count(results)
        data = {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "summary": counts._asdict(),   # NamedTuple's built-in dict conversion
            "assets": [
                {"asset_path": asset[0].asset_path, "checks": [self._result_to_dict(r) for r in asset]}
                for asset in results
                if asset
            ],
        }
        with open(output_path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)