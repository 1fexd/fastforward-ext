import urllib.parse
from abc import ABC
from typing import Dict, TextIO, List

from fwutil.FileWriter import FileWriter

from helper.writer import RegexWriter, KotlinRegexWriter, TypescriptRegexWriter, TextWriter


class Builder(ABC):
    def __init__(self, regex_writer: RegexWriter):
        self.regex_writer = regex_writer

    def write(self, writer: FileWriter, rules: Dict[str, List[str]]):
        pass


class TypescriptBuilder(Builder):
    def __init__(self):
        super().__init__(TypescriptRegexWriter())

    def write(self, writer: FileWriter, rules: Dict[str, List[str]]):
        writer.write_multiline(f"""
            export const trackers = [
                {self.regex_writer.to_comma_separated_str(rules["tracker"])}
            ];
        """, clean=True)


class KotlinBuilder(Builder):
    def __init__(self):
        super().__init__(KotlinRegexWriter())

    def write(self, writer: FileWriter, rules: Dict[str, List[str]]):
        map_items_str = ",".join([
            f""""{rule}" to listOf({self.regex_writer.to_comma_separated_str(rules[rule])})"""
            for rule in rules
        ])

        writer.write_multiline(f"""
            package fe.fastforwardkt
            
            object FastForwardRules {{
                 val rules = mapOf({map_items_str})
            }}
        """, clean=True)


class TextTrackerHostnameBuilder(Builder):
    def __init__(self):
        super().__init__(TextWriter())

    @staticmethod
    def __regex_tracker_to_hostname(regex_tracker: str):
        tracker = regex_tracker.replace(".*", "").replace("\\", "").replace("?://", "://")

        if tracker.startswith("://"):
            tracker = f"https{tracker}"

        return urllib.parse.urlparse(tracker).hostname

    def write(self, writer: FileWriter, rules: Dict[str, List[str]]):
        writer.write_list(rules["tracker"], separator="\n", transform=self.__regex_tracker_to_hostname)


class TextTrackerRegexBuilder(Builder):
    def __init__(self):
        super().__init__(TextWriter())

    def write(self, writer: FileWriter, rules: Dict[str, List[str]]):
        writer.write_list(rules["tracker"], separator="\n")
