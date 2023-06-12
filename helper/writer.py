from abc import ABC
from typing import List


class RegexWriter(ABC):
    def str_to_regex(self, regex: str) -> str:
        pass

    def strs_to_regex(self, regexes: List[str]) -> List[str]:
        return [self.str_to_regex(regex) for regex in regexes]

    def to_comma_separated_str(self, regexes: List[str]) -> str:
        return ",".join(self.strs_to_regex(regexes))


class KotlinRegexWriter(RegexWriter):
    def str_to_regex(self, regex: str) -> str:
        return f"""Regex("{regex}", RegexOption.IGNORE_CASE)"""


class TypescriptRegexWriter(RegexWriter):
    def str_to_regex(self, regex: str) -> str:
        return f"""new RegExp("{regex}", "i")"""
