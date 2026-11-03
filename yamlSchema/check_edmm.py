#!/usr/bin/env python3
"""Checks EDMM models in the YAML serialization of the DeMAF.

Each model is checked in two steps, and each finding is reported as an error or a warning.

Step 1: The model is validated against edmm.schema.json. Every schema violation is an
error, reported with its location in the model (the path of keys and list indices) and the
violated rule. A file that cannot be read as UTF-8 encoded YAML is a single error. If the
model violates the schema, step 2 is skipped, because its checks require a valid structure.

Step 2: Violations of the following constraints, which JSON Schema cannot express, are
errors, reported with the list and the name of the element:

- the names of components, relations, component types, and relation types are unique, and
  so are the property keys within each element and each type
- the type of every component and relation is defined in the model, i.e., in
  component_types or relation_types
- the source and the target of every relation are components of the model and not the
  same component
- every component type hierarchy ends at BaseType and every relation type hierarchy at
  DependsOn, without cycles
- every component and relation has all properties that the property definitions of its
  type and its supertypes require, unless the property definition has a default value
- every property value matches the type of its property definition

The following findings are warnings, because they do not make the model inconsistent:

- required properties of a component or relation that are not assigned, so that the
  default value of their property definition applies; an empty string counts as no
  default value, because the DeMAF writes it for properties without a default value
- properties of a component or relation that no property definition of its type or its
  supertypes declares
- types that are neither the type of a component or relation nor the supertype of another
  type, except for the predefined types of the DeMAF type system in ../edmm

Usage: python3 check_edmm.py [--strict] MODEL.yaml [MODEL.yaml ...]
Requires PyYAML and jsonschema (pip install -r requirements.txt). The exit code is 1 if a
model has errors, or warnings with --strict, and 0 otherwise.
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import jsonschema
    import yaml
except ImportError as error:
    sys.exit(f"{error.name} is missing: pip install -r {Path(__file__).with_name('requirements.txt')}")

SCHEMA = Path(__file__).with_name("edmm.schema.json")
TYPE_SYSTEM = Path(__file__).resolve().parent.parent / "edmm"
ROOT_TYPES = {"component_types": "BaseType", "relation_types": "DependsOn"}
VALUE_TYPES = {
    "STRING": lambda v: isinstance(v, str),
    "INTEGER": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "DOUBLE": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "BOOLEAN": lambda v: isinstance(v, bool),
}


def entries(items: list) -> list[tuple[str, object]]:
    """Name and body of each single-key entry of a list."""
    return [next(iter(item.items())) for item in items]


def predefined_types() -> set[str]:
    """Names of the types of the DeMAF type system, which every EDMM model of the DeMAF includes."""
    names = set()
    for path in TYPE_SYSTEM.glob("*.yaml"):
        definitions = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for kind in ROOT_TYPES:
            names.update(name for name, _ in entries(definitions.get(kind) or []))
    return names


class Checker:
    def __init__(self, model: dict, predefined: set[str]):
        self.model = model
        self.predefined = predefined
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def check(self) -> None:
        types = {kind: self.check_types(kind) for kind in ROOT_TYPES}
        components = self.unique("components")
        for name, component in components.items():
            self.check_element(f"components/{name}", component, types["component_types"], "component_types")
        for name, relation in self.unique("relations").items():
            path = f"relations/{name}"
            self.check_element(path, relation, types["relation_types"], "relation_types")
            for end in ("source", "target"):
                if relation[end] not in components:
                    self.errors.append(f"{path}: {end} '{relation[end]}' is not a component")
            if relation["source"] == relation["target"]:
                self.errors.append(f"{path}: source and target are the same component")
        self.check_unused_types(types)

    def unique(self, key: str) -> dict:
        result = {}
        for name, body in entries(self.model[key]):
            if name in result:
                self.errors.append(f"{key}/{name}: name is not unique")
            result[name] = body
        return result

    def check_types(self, kind: str) -> dict:
        types = self.unique(kind)
        for name, definition in types.items():
            seen, current = [name], definition["extends"]
            while current != "-":
                if current not in types:
                    self.errors.append(f"{kind}/{name}: supertype '{current}' is not defined")
                    break
                if current in seen:
                    self.errors.append(f"{kind}/{name}: type hierarchy contains a cycle: {' -> '.join(seen + [current])}")
                    break
                seen.append(current)
                current = types[current]["extends"]
            else:
                if seen[-1] != ROOT_TYPES[kind]:
                    self.errors.append(f"{kind}/{name}: type hierarchy ends at '{seen[-1]}' instead of '{ROOT_TYPES[kind]}'")
            self.unique_keys(f"{kind}/{name}", definition.get("properties", []))
        return types

    def unique_keys(self, path: str, properties: list) -> None:
        keys = [key for key, _ in entries(properties)]
        for key in sorted({k for k in keys if keys.count(k) > 1}):
            self.errors.append(f"{path}: property '{key}' is defined more than once")

    def definitions(self, type_name: str, types: dict) -> dict:
        """Property definitions of a type including those of its supertypes; subtypes override."""
        chain, current = [], type_name
        while current in types and current not in chain:
            chain.append(current)
            current = types[current]["extends"]
        result = {}
        for name in reversed(chain):
            result.update(entries(types[name].get("properties", [])))
        return result

    def check_element(self, path: str, element: dict, types: dict, kind: str) -> None:
        type_name = element["type"]
        if type_name == "-":
            self.errors.append(f"{path}: has no type")
            return
        if type_name not in types:
            self.errors.append(f"{path}: type '{type_name}' is not defined in {kind}")
            return
        properties = element.get("properties", [])
        self.unique_keys(path, properties)
        values = dict(entries(properties))
        definitions = self.definitions(type_name, types)
        for key, definition in definitions.items():
            if not definition["required"] or key in values:
                continue
            # As in TOSCA, the default value applies to a property that is not assigned. The DeMAF
            # writes an empty string for properties without a default value, so it is none.
            if definition.get("default_value", "") != "":
                self.warnings.append(
                    f"{path}: required property '{key}' of type '{type_name}' is not assigned, its default value applies")
            else:
                self.errors.append(f"{path}: required property '{key}' of type '{type_name}' is missing")
        for key, value in values.items():
            if key not in definitions:
                self.warnings.append(f"{path}: property '{key}' is not defined by type '{type_name}' or its supertypes")
            elif not VALUE_TYPES[definitions[key]["type"]](value):
                self.errors.append(f"{path}: value {value!r} of property '{key}' is not of type {definitions[key]['type']}")

    def check_unused_types(self, types: dict) -> None:
        used = {
            "component_types": {c["type"] for _, c in entries(self.model["components"])},
            "relation_types": {r["type"] for _, r in entries(self.model["relations"])},
        }
        for kind, definitions in types.items():
            parents = {d["extends"] for d in definitions.values()}
            for name in definitions:
                if name not in used[kind] and name not in parents and name not in self.predefined:
                    self.warnings.append(f"{kind}/{name}: type is neither used nor extended")


def schema_message(error: jsonschema.ValidationError) -> str:
    location = "/".join(map(str, error.absolute_path)) or "(root)"
    if error.validator in ("minProperties", "maxProperties"):
        # The default message repeats the complete element
        return f"{location}: an entry must be a map with exactly one key, the name of the element"
    if error.validator == "oneOf" and "operations" in error.absolute_path:
        # The default message does not name the alternatives
        return (f"{location}: an operation must be null, the file URI of its artifact, or a map "
                "(with optional description, metadata, and artifacts)")
    return f"{location}: {error.message if len(error.message) <= 200 else error.message[:200] + '...'}"


def check_file(path: Path, validator: jsonschema.Draft7Validator, predefined: set[str]) -> tuple[list[str], list[str]]:
    try:
        model = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as error:
        return [f"cannot be read as YAML: {error}"], []
    schema_errors = sorted(validator.iter_errors(model), key=lambda e: list(e.absolute_path))
    if schema_errors:
        return [schema_message(e) for e in schema_errors], []
    checker = Checker(model, predefined)
    checker.check()
    return checker.errors, checker.warnings


def plural(count: int, word: str) -> str:
    return f"{count} {word}{'' if count == 1 else 's'}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Check EDMM models in the YAML serialization of the DeMAF.")
    parser.add_argument("models", nargs="+", type=Path, metavar="MODEL.yaml")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args()

    validator = jsonschema.Draft7Validator(json.loads(SCHEMA.read_text(encoding="utf-8")))
    predefined = predefined_types()
    failed = False
    for path in args.models:
        errors, warnings = check_file(path, validator, predefined)
        for message in errors:
            print(f"{path}: error: {message}")
        for message in warnings:
            print(f"{path}: warning: {message}")
        print(f"{path}: {plural(len(errors), 'error')}, {plural(len(warnings), 'warning')}")
        failed |= bool(errors) or (args.strict and bool(warnings))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
