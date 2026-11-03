# YAML Schema for EDMM Models

This folder provides a schema and a checker for EDMM models in the YAML serialization that the DeMAF creates:

- [edmm.schema.json](edmm.schema.json): a [JSON Schema](https://json-schema.org/) (using version draft-07) for the structure of EDMM models, against which YAML tools validate YAML files.
- [check_edmm.py](check_edmm.py): a script that validates EDMM models against the schema and checks further constraints

See below for usage, editor integrations, and explanations on how EDMM models are structured and how the validation works.

## Usage

The script requires Python 3.10 or later with PyYAML and jsonschema.
Install the dependencies into a virtual environment and test all examples in [../examples](../examples/):

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 check_edmm.py ../examples/*/*_edmm.yaml
```

## Schema Validation in Editors

Editors with YAML language support, such as Visual Studio Code with the [YAML extension](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml), validate EDMM models against the schema and offer completion while editing.
Either add the following line at the top of an EDMM model:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/UST-DeMAF/demaf-type-definitions/main/yamlSchema/edmm.schema.json
```

or associate the schema with file patterns in the settings of the editor, e.g., for all EDMM models of the examples:

```json
"yaml.schemas": {
  "https://raw.githubusercontent.com/UST-DeMAF/demaf-type-definitions/main/yamlSchema/edmm.schema.json": ["*_edmm.yaml"]
}
```

A local path to `edmm.schema.json` works as well.

## Structure of EDMM Models

An EDMM model has the top-level keys `properties`, `components`, `relations`, `component_types`, and `relation_types`, each with a list as value, which may be empty.
Optionally, it has a `version`, a `description`, and `metadata`.
Each entry of the lists is a map with exactly one key, the name of the element, whose value defines the element.
The following example shows a complete EDMM model with an application that connects to a database:

```yaml
version: "1.0"
description: "An application that connects to a database"
properties: []
components:
  - my-app:
      type: "my-app-SoftwareApplication"
      metadata:
        team: "example"
      properties:
        - port: 8080
      operations:
        - start:
            artifacts:
              - file:
                  name: "start.sh"
      artifacts:
        - docker_image:
            name: "example/my-app:1.0"
            fileURI: "https://hub.docker.com/r/example/my-app"
            digest: "sha256:0123abcd"
  - my-database:
      type: "DatabaseSystem"
      description: "The database of my-app"
      properties: []
      operations: []
      artifacts: []
relations:
  - my-app_ConnectsTo_my-database:
      type: "ConnectsTo"
      source: "my-app"
      target: "my-database"
      properties: []
      operations: []
component_types:
  - BaseType:
      extends: "-"
      properties: []
      operations: []
  - SoftwareApplication:
      extends: "BaseType"
      properties: []
      operations: []
  - DatabaseSystem:
      extends: "SoftwareApplication"
      properties: []
      operations: []
  - my-app-SoftwareApplication:
      extends: "SoftwareApplication"
      properties:
        - port:
            type: "INTEGER"
            description: "Port on which my-app listens"
            required: true
            default_value: 8080
      operations:
        - start: ~
relation_types:
  - DependsOn:
      extends: "-"
      properties: []
      operations: []
  - ConnectsTo:
      extends: "DependsOn"
      properties: []
      operations: []
```

- **Properties** of the model, components, and relations assign values: each maps a property key to its value, which is a string, integer, double, or boolean (`port: 8080` of `my-app`).
- **Property definitions** of component and relation types declare which properties the elements of the type have: each maps a property key to its `type` (`STRING`, `INTEGER`, `DOUBLE`, or `BOOLEAN`), whether it is `required`, and optionally a `default_value` of that type (`port` of `my-app-SoftwareApplication`).
  A component or relation is defined by the property definitions of its type and of all supertypes of its type, and its properties assign values to them.
- **Operations** of components, relations, and types map the operation name to its definition: either `~` (null) if the operation is only declared (`start` of `my-app-SoftwareApplication`), the file URI of the artifact that implements it (short form), or a map with optional `description`, `metadata`, `artifacts`, and further keys (long form, `start` of `my-app`).
  The models service writes the string `"~"` for operations of types, which the schema accepts as a short form.
- **Artifacts** map the artifact type (e.g., `docker_image` or `file`) to the artifact, which has a `name` and may have a `fileURI` and further properties (`digest` of the image of `my-app`).
- **Descriptions and metadata** are optional on components, relations, types, property definitions, and operations in long form: a `description` is a string or null, and `metadata` is a map of strings (`metadata` of `my-app`).
- **Lists of elements**: components, relations, and types may omit their `properties`, `operations`, and `artifacts` (components only); the models service always writes them, if necessary as empty lists.
- **Further keys** are allowed in artifacts and in operations in long form.
  The model, components, relations, types, and property definitions only allow the keys described above, so that misspelled keys are detected; use `metadata` for additional information.
- `"-"` denotes a missing type, source, target, parent type (`extends`), or file URI.

## Checking EDMM Models

JSON Schema validates the structure of each element, but not the references between elements.
`check_edmm.py` therefore checks each model in two steps and reports each finding as an error or a warning.

**Step 1: Schema validation.** The model is validated against `edmm.schema.json`.
Every schema violation is an error, reported with its location in the model (the path of keys and list indices) and the violated rule, e.g.:

```text
model.yaml: error: components/4/backend: Additional properties are not allowed ('replicas' was unexpected)
```

A file that cannot be read as UTF-8 encoded YAML is reported as a single error.
If the model violates the schema, step 2 is skipped, because its checks require a valid structure.

**Step 2: Constraints.** Violations of the following constraints are errors:

- the names of components, relations, component types, and relation types are unique, and so are the property keys within each element and each type,
- the type of every component and relation is defined in the model, i.e., in `component_types` or `relation_types`,
- the source and the target of every relation are components of the model and not the same component,
- every component type hierarchy ends at `BaseType` and every relation type hierarchy at `DependsOn`, without cycles,
- every component and relation has all properties that the property definitions of its type and its supertypes require, unless the property definition has a default value, and
- every property value matches the type of its property definition.

The following findings are warnings, because they do not make the model inconsistent:

- required properties of a component or relation that are not assigned, so that the default value of their property definition applies (as in TOSCA); an empty string counts as no default value, because the DeMAF writes it for properties without a default value,
- properties of a component or relation that no property definition of its type or its supertypes declares, and
- types that are neither the type of a component or relation nor the supertype of another type, except for the predefined types of the [DeMAF type system](../edmm/).

Errors and warnings of step 2 are reported with the list and the name of the element, e.g.:

```text
model.yaml: error: relations/my-app_ConnectsTo_my-database: target 'my-db' is not a component
model.yaml: warning: components/my-app: property 'version' is not defined by type 'my-app-SoftwareApplication' or its supertypes
```

For each model, the script ends with a summary line such as `model.yaml: 1 error, 1 warning`.
It exits with code 1 if a model has errors, or with `--strict` also if a model has warnings, and with code 0 otherwise.
