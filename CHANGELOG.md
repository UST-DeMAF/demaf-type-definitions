# Changelog of the Type Definitions

Changes to the component and relation types in [edmm/](edmm/) and [tosca/](tosca/).
Changes to the example models are listed in [examples/CHANGELOG.md](examples/CHANGELOG.md).

## Type Descriptions

- Every component and relation type, and the properties `storage_size` (`Storage`) and `location` (`AttachesTo`), have a description. The descriptions of `Compute` and `Platform` are replaced: `Compute` describes machines, and `Platform` describes platforms in general.
- `ContainerPlatform` derives from `Platform` instead of `BaseType`.
- `localhost-type` is removed. It is not an abstract type but the type the DeMAF generates for the Ansible host `localhost`; the OTEL-Shop-Ansible example model still defines it.
- The TOSCA types in [tosca/](tosca/) are aligned with the EDMM types: they get the same descriptions and changes, and `Compute` and `Platform` are added.
- `yamlSchema/check_edmm.py` has the option `--type-descriptions`, which warns about types of the type system whose descriptions in a model differ from the type definitions.
- The README lists all descriptions and shows the type hierarchies as Mermaid diagrams instead of the images in [diagrams/](diagrams/), which are no longer maintained.
