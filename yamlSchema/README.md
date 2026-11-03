# YAML Schema for EDMM Models

This folder provides a schema and a checker for EDMM models in the YAML serialization that the DeMAF creates, as written by the `yamlserializer` package of the [models service](<https://github.com/UST-DeMAF/models-service>):

- [edmm.schema.json](edmm.schema.json): a [JSON Schema](https://json-schema.org/) for the structure of EDMM models, against which YAML tools validate YAML files.
  JSON Schema is versioned in drafts; the schema uses draft-07, the version that editors and validators support most widely.
- [check_edmm.py](check_edmm.py): a script that validates EDMM models against the schema and checks further constraints

## Structure of EDMM Models

An EDMM model has the top-level keys `properties`, `components`, `relations`, `component_types`, and `relation_types`, each with a list as value, which may be empty.
Each entry of these lists is a map with exactly one key, the name of the element, whose value defines the element.
The following example shows a complete EDMM model with an application that connects to a database:

```yaml
properties: []
components:
  - my-app:
      type: "my-app-SoftwareApplication"
      description: null
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
  - my-database:
      type: "DatabaseSystem"
      description: null
      properties: []
      operations: []
      artifacts: []
relations:
  - my-app_ConnectsTo_my-database:
      type: "ConnectsTo"
      description: null
      source: "my-app"
      target: "my-database"
      properties: []
      operations: []
component_types:
  - BaseType:
      extends: "-"
      description: null
      properties: []
      operations: []
  - SoftwareApplication:
      extends: "BaseType"
      description: null
      properties: []
      operations: []
  - DatabaseSystem:
      extends: "SoftwareApplication"
      description: null
      properties: []
      operations: []
  - my-app-SoftwareApplication:
      extends: "SoftwareApplication"
      description: null
      properties:
        - port:
            type: "INTEGER"
            required: true
            default_value: 8080
      operations:
        - start: "~"
relation_types:
  - DependsOn:
      extends: "-"
      description: null
      properties: []
      operations: []
  - ConnectsTo:
      extends: "DependsOn"
      description: null
      properties: []
      operations: []
```

- **Properties** of the model, components, and relations assign values: each maps a property key to its value, which is a string, integer, double, or boolean (`port: 8080` of `my-app`).
- **Property definitions** of component and relation types declare which properties the elements of the type have: each maps a property key to its `type` (`STRING`, `INTEGER`, `DOUBLE`, or `BOOLEAN`), whether it is `required`, and optionally a `default_value` of that type (`port` of `my-app-SoftwareApplication`).
  A component or relation is defined by the property definitions of its type and of all supertypes of its type, and its properties assign values to them.
- **Operations** of components and relations map the operation name to the `artifacts` that implement it.
  Operations of types only declare the operation name, which the models service maps to the string `"~"`.
- **Artifacts** map the artifact type (e.g., `docker_image` or `file`) to the `name` of the artifact and optionally its `fileURI`.
- `"-"` denotes a missing type, source, target, parent type (`extends`), or file URI.

## Validation in the Editor

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

## Checking EDMM Models

JSON Schema validates the structure of each element, but not the references between elements.
In addition to validating the structure, `check_edmm.py` therefore checks that

- the names of components, relations, component types, and relation types are unique, and so are the property keys within each element and each type,
- the type of every component and relation is defined in the model, i.e., in `component_types` or `relation_types`,
- the source and the target of every relation are components of the model and not the same component,
- every component type hierarchy ends at `BaseType` and every relation type hierarchy at `DependsOn`, without cycles,
- every component and relation has all properties that the property definitions of its type and its supertypes require, and
- every property value matches the type of its property definition.

In addition, it warns about

- properties of a component or relation that no property definition of its type or its supertypes declares, and
- types that are neither the type of a component or relation nor the supertype of another type, except for the predefined types of the [DeMAF type system](../edmm/).

The script requires Python 3.10 or later with PyYAML and jsonschema.
Install the dependencies into a virtual environment and test all examples in [../examples](../examples/):

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 check_edmm.py ../examples/*/*_edmm.yaml
```

It prints the errors and warnings of each model and exits with code 1 if a model has errors, or with `--strict` also if it has warnings.
