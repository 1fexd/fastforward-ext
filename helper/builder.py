import time
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

        now = int(time.time() * 1000.0)

        writer.write_multiline(f"""
            package fe.fastforwardkt
            
            object FastForwardRules {{
                 const val fetchedAt = {now}L
                 val rules = mapOf({map_items_str})
            }}
        """, clean=True)


class TextTrackerHostnameBuilder(Builder):
    def __init__(self):
        super().__init__(TextWriter())

    @staticmethod
    def __regex_tracker_to_hostname(regex_tracker: str) -> str:
        regex_tracker = regex_tracker.replace("https?:\\/\\/", "").replace("(?:.+\\.)?", "").replace(".*:\\/\\/", "")
        has_any_path_idx = regex_tracker.rfind("\\/.*")
        if has_any_path_idx != -1:
            regex_tracker = regex_tracker[0:has_any_path_idx]

        # if regex_tracker.startswith(".*"):
        #     regex_tracker = regex_tracker[2:]

        regex_tracker = regex_tracker.replace(".*", "").replace(".+", "")
        regex_tracker = regex_tracker.replace("\\", "")
        #
        # print(regex_tracker)

        # tracker = regex_tracker.replace("\\", "").replace("?://", "://").replace("(?:.+\\.)?", "")
        #
        # if tracker.startswith("://"):
        #     tracker = f"https{tracker}"
        print(regex_tracker)
        try:
            urllib.parse.urlparse(regex_tracker).hostname
        except Exception as e:
            print(e)
        return regex_tracker
        # return urllib.parse.urlparse(regex_tracker).hostname

    def write(self, writer: FileWriter, rules: Dict[str, List[str]]):
        writer.write_list(rules["tracker"], separator="\n", transform=self.__regex_tracker_to_hostname)


class TextTrackerRegexBuilder(Builder):
    def __init__(self):
        super().__init__(TextWriter())

    def write(self, writer: FileWriter, rules: Dict[str, List[str]]):
        writer.write_list(rules["tracker"], separator="\n")
