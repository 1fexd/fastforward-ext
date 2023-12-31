import json

from fwutil.FileWriter import open_file

from helper.builder import TypescriptBuilder, KotlinBuilder, TextTrackerHostnameBuilder, TextTrackerRegexBuilder
from wildcard import wildcard_to_regex, host_to_regex

with open("fastforward/rules.json", "r") as file:
    rules = json.load(file)

with open("fastforward/additional_rules.json", "r") as file:
    additional_rules = json.load(file)

result_rules = {}
for rule in rules:
    list_items = rules[rule]
    if len(list_items) > 0:
        if rule not in ["tracker_force_http"]:
            result_rules[rule] = [wildcard_to_regex(wildcard) for wildcard in list_items]
        else:
            result_rules[rule] = [host_to_regex(host) for host in list_items]

for rule in additional_rules:
    result_rules[rule] += additional_rules[rule]

__BUILDER = {
    TypescriptBuilder(): "tracker.ts",
    KotlinBuilder(): "FastForwardRules.kt",
    TextTrackerHostnameBuilder(): "tracker_hostnames.txt",
    TextTrackerRegexBuilder(): "tracker_regex.txt",
}

with open("rules.json", "w") as file:
    json.dump(result_rules, file)

for builder, file in __BUILDER.items():
    with open_file(f"output/{file}") as fw:
        builder.write(fw, result_rules)
