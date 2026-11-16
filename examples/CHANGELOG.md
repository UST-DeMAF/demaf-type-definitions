# Changelog of the Example EDMM Models

The example EDMM models (`*_edmm.yaml`) are the manually created expected models of the CoopIS 2025 evaluation.
They are versioned as a set:

| Version | State | Content |
| --- | --- | --- |
| v1 | git tag `expected-models-v1` | The models as published with the supplemental material of the CoopIS 2025 evaluation, byte-identical. |
| v1.1 | in progress | Consistency fixes only, each logged below with its evidence in the deployment model and what found it. No fix changes which components or relations exist or which types they have, so the metrics of the CoopIS 2025 evaluation are unchanged. |
| v2 | planned | Scope extension (more properties, new cases) under an annotation guideline that is frozen before it is applied. |

## v1.1

- **Meitrex**: The relation `dapr-sidecar-injector_ConnectsTo_graphql_gateway` targeted `graphql_gateway`, which is no component; the component is `gits-gateway` (type `graphql_gateway-SoftwareApplication`, image `ghcr.io/it-rex-platform/graphql_gateway`, defined in `deploymentModel/gateway.tf` like the other dapr-enabled services the injector connects to). The relation now targets `gits-gateway` and is named accordingly. Found by `check_edmm.py` and the comparison script of the LLM-transformation evaluation (2026-11-16). Metrics unchanged: the actual model contains no injector-to-gateway relation under either name, so the relation stays a false negative.
- **OTEL-Shop-Ansible**: The component type `adservice-SoftwareApplication` of the component `adservice` was not defined; instead, the type definition named `accountingservice-SoftwareApplication` contained adservice's property definitions (`service.name=adservice`, `AD_SERVICE_PORT`), so the accountingservice's `KAFKA_SERVICE_ADDR` was undeclared as well. The mislabeled definition is renamed to `adservice-SoftwareApplication`, and `accountingservice-SoftwareApplication` is added with the accountingservice's five properties (evidence: the `accountingservice` role of the deployment model and the component's properties; the OTEL-Shop-Kubernetes model declares `KAFKA_SERVICE_ADDR` for its accountingservice likewise). Found by `check_edmm.py` (2026-11-16). Metrics unchanged: component types enter the evaluation only through Q2, which compares the types assigned to components, and those are untouched.
