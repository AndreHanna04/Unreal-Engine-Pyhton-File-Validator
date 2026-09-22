

import argparse
from Validator import ValidationRunner, Config
from Validator.context.filesystem import FileSystemcontext
from Validator.reporter import Reporter
from Validator.rules.base import RuleType, Severity
from Validator.registry import registry

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="validates the chosen directory")
    parser.add_argument("--directory", type=str, default=".")
    parser.add_argument("--summary_only", action="store_true")
    parser.add_argument("--config", "-c", default=None, metavar="FILE")
    parser.add_argument("--rule_list", "-r", type=str, default=None,
                         metavar="RULE_NAME,RULE_NAME,...",
                         help="comma-separated rule names, e.g. extention_rule,filesize_rule")
    parser.add_argument("--rule_type", "-rt", type=str, default=None,
                         choices=[t.name for t in RuleType], metavar="RULE_TYPE")
    parser.add_argument("--rule_severity", "-rs", type=str, default=None,
                         choices=[s.name for s in Severity], metavar="SEVERITY")
    parser.add_argument("--log", type=str, default=None, metavar="FILE")
    args = parser.parse_args()


    rule_type = RuleType[args.rule_type] if args.rule_type else None
    rule_severity = Severity[args.rule_severity] if args.rule_severity else None

    rule_list = None
    if args.rule_list:
        registry.discover()
        rule_list = []
        for name in (n.strip() for n in args.rule_list.split(",")):
            if not name:
                continue
            rule_cls = registry.get_rule(name)
            if rule_cls is None:
                parser.error(f"Unknown rule name: '{name}'")
            rule_list.append(rule_cls)

    context = FileSystemcontext(args.directory)
    config = Config(config_path=args.config)
    reporter = Reporter()
    runner = ValidationRunner(config, context, rule_type, rule_severity, rule_list )
    results = runner.run_validation(summary_only=args.summary_only)
    reporter.print_summary(results)
    if args.log:
        reporter.export_results_json(results, args.log)
