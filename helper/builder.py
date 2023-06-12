from abc import ABC
from typing import Dict, TextIO, List

from fwutil.FileWriter import FileWriter

from helper.writer import RegexWriter, KotlinRegexWriter, TypescriptRegexWriter


class Builder(ABC):
    def __init__(self, regex_writer: RegexWriter):
        self.regex_writer = regex_writer

    def write(self, writer: FileWriter, rules: Dict[str, List[str]]):
        pass


class TypescriptBuilder(Builder):
    def __init__(self, **kwargs):
        super(TypescriptBuilder, self).__init__(TypescriptRegexWriter())

    def write(self, writer: FileWriter, rules: Dict[str, List[str]]):
        writer.write(f"""
            export const trackers = [
                {self.regex_writer.to_comma_separated_str(rules["tracker"])}
            ];
        """, clean=True)


class KotlinBuilder(Builder):
    def __init__(self, **kwargs):
        super(KotlinBuilder, self).__init__(KotlinRegexWriter())

    def write(self, writer: FileWriter, rules: Dict[str, List[str]]):
        map_items_str = ",".join([
            f""""{rule}" to listOf({self.regex_writer.to_comma_separated_str(rules[rule])})"""
            for rule in rules
        ])

        writer.write(f"""
            package fe.fastforwardkt
            
            object FastforwardRules {{
                 val rules = mapOf({map_items_str})
            }}
        """, clean=True)
