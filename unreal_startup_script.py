import unreal
from .Validator.reporter import Reporter
from .Validator.config import Config
from .Validator.runner import ValidationRunner, ValidationResult
from .Validator.context.unreal import UnrealContext
from .settings import ValidatorSettings
from unreal import Name, Text

@unreal.uclass()
class ValidateFolderScript(unreal.ToolMenuEntryScript):

    @unreal.ufunction(override=True)
    def execute(self, context):
        folders = list(
        unreal.EditorUtilityLibrary.get_selected_path_view_folder_paths()
        )
        if not folders:
            unreal.log_warning("[Validator] No folder selected.")
            return

        for folder in folders:
            folder_path = folder[4:] if folder.startswith("/All") else folder
            reporter = Reporter()
            runner = ValidationRunner(Config(), context=UnrealContext(folder_path))
            report = runner.run_validation()
            count = reporter.count(report)
            reporter.print_summary(report)

            for result in report:
                for r in result:
                    if not r.validation_pass:
                        unreal.log_error(str(r))

            unreal.log(f"[Validator] {folder_path}: "
            f"{count.asset_pass_count} passed assets / "
            f"{count.rule_pass_count} passed rules/ "
            f"{count.asset_fail_count} failed assets / "
            f"{count.rule_fail_count} failed rules /"
            f"{count.rule_skip_count} skipped rules")


def register_folder_menu() -> None:
    menu_name = "ContentBrowser.FolderContextMenu"
    entry = ValidateFolderScript()
    entry.init_entry(
        owner_name=Name(menu_name), menu=Name(menu_name),
        section=Name("PathViewFolderOptions"),
        name=Name("ValidateFolder"), label=Text("Validate Assets"),
    )
    entry.register_menu_entry()
    unreal.ToolMenus.get().refresh_all_widgets()


try:
    register_folder_menu()
except Exception as exc:
    unreal.log_error(f"[Validator] Menu registration failed: {exc}")