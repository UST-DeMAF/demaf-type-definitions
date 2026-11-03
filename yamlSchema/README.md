# YAML Schema for EDMM Models

This folder provides a schema and a checker for EDMM models in the YAML serialization that the DeMAF creates, as written by the `yamlserializer` package of the [models service](<https://github.com/UST-DeMAF/models-service>):

- [edmm.schema.json](edmm.schema.json): a JSON Schema (draft-07), which YAML tools use to validate YAML files, for the structure of EDMM models
- [check_edmm.py](check_edmm.py): a script that validates EDMM models against the schema and checks their consistency

## Structure of EDMM Models

An EDMM model has the top-level keys `properties`, `components`, `relations`, `component_types`, and `relation_types`, each with a list as value.
Each entry of these lists is a map with exactly one key, the name of the element, whose value defines the element:

```yaml
components:
  - backend:
      type: "backend-SoftwareApplication"
      description: null
      properties:
        - containerPort: 8080
      operations: []
      artifacts:
        - docker_image:
            name: "t2project/backend:main"
            fileURI: "https://hub.docker.com/r/t2project/backend"
relations:
  - backend_ConnectsTo_postgres:
      type: "ConnectsTo"
      description: null
      source: "backend"
      target: "postgres"
      properties: []
      operations: []
component_types:
  - backend-SoftwareApplication:
      extends: "SoftwareApplication"
      description: null
      properties:
        - containerPort:
            type: "INTEGER"
            required: true
            default_value: 8080
      operations: []
```

- **Properties** of the model, components, and relations map a property key to a string, integer, double, or boolean value.
- **Operations** of components and relations map the operation name to its `artifacts`; operations of types map the operation name to `~`.
- **Artifacts** map the artifact type (e.g., `docker_image` or `file`) to its `name` and `fileURI`.
- **Property definitions** of types have a `type` (`STRING`, `INTEGER`, `DOUBLE`, or `BOOLEAN`), whether they are `required`, and optionally a `default_value` of that type.
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

- the names of components, relations, and types are unique, and so are the property keys of each element,
- every component and relation has a type that the model defines,
- every relation connects two different components of the model,
- every type hierarchy ends at `BaseType` (component types) or `DependsOn` (relation types), without cycles,
- every component and relation has the properties that its type and its supertypes require, and
- every property value matches the type of its property definition.

As warnings, it reports properties that no type of an element defines and types that are neither used nor extended, except for the predefined types of the [DeMAF type system](../edmm/).

The script requires Python 3.10 or later with PyYAML and jsonschema:

```shell
pip install -r requirements.txt
python3 check_edmm.py ../examples/*/*_edmm.yaml
```

It prints the errors and warnings of each model and exits with code 1 if a model has errors, or with `--strict` also if it has warnings.
