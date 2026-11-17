# Changelog of the Example EDMM Models

The example EDMM models (`*_edmm.yaml`) are versioned as a set:

| Version | State | Content |
| --- | --- | --- |
| v1 | git tag `edmm-model-v1` | The models as published with the supplemental material of the CoopIS 2025 evaluation ([doi:10.5281/zenodo.15882026](https://doi.org/10.5281/zenodo.15882026)), byte-identical. |
| v1.1 | git tag `edmm-model-v1.1` | Consistency fixes only, based on errors and warnings reported by the EDMM YAML schema and the check script. Each fix is logged below with its evidence in the deployment model and what found it. |
| v1.2 | git tag `edmm-model-v1.2` | Helm chart versions pinned in the deployment models to the versions of the rendered templates in `helmTemplates/`. The EDMM models are unchanged. |
| v1.3 | git tag `edmm-model-v1.3` | Repair of the OTEL-Shop-Ansible deployment model and the corresponding changes in its EDMM model. |
| v2 | planned | Scope extension (more properties, new cases). |

## v1.3 Repair OTEL-Shop-Ansible

- **OTEL-Shop-Ansible**: The role `productcatalogservice` ran the official image `ghcr.io/open-telemetry/demo:1.11.1-productcatalogservice`, which does not use the MongoDB that the role configures (`MONGO_*` variables) and that the example adds to the demo. The role now runs our image `ghcr.io/ust-demaf/demo:1.11.1-productcatalogservice` (`image_name` in `deploymentModel/roles/productcatalogservice/defaults/main.yaml`), like the OTEL-Shop-Kubernetes and OTEL-Shop-Terraform examples. In the EDMM model, the eight image references in the artifacts and operations of `productcatalogservice` changed accordingly.
- **OTEL-Shop-Ansible**: The two post tasks of `deploymentModel/main.yaml`, "Ensure services are started" and "Ensure services are enabled to start at boot", used `community.general.launchd`, which manages launchd services on macOS hosts, not the Docker containers that the roles create; their lists also contained `frauddetectionserice` instead of `frauddetectionservice`. The roles already start the containers with `docker_container`, and `restart_policy: unless-stopped` restarts them at boot, so both post tasks are removed. In the EDMM model, the two corresponding operations of `localhost` are removed.

**Known issue**: In OTEL-Shop-Ansible and OTEL-Shop-Terraform, `frontendproxy` and `loadgenerator` depend on each other (role dependencies in `roles/*/meta/main.yaml`, `depends_on` in `main.tf`), because the two services connect to each other. Ansible and Terraform reject this cycle (`ansible-playbook --syntax-check`, `terraform validate`), so these two deployment models cannot be deployed as they are. The EDMM models are not affected. The cycle will be resolved in v2.

## v1.2 Pin Helm Chart Versions

The deployment models of Meitrex, T2Store-Microservices, and T2Store-Modulith installed 16 of their 17 Helm releases without a chart version, so they installed whatever version was current, which differs from the versions the EDMM models describe.
Each release is now pinned to the chart version of its rendered template in `helmTemplates/` (from the `helm.sh/chart` label; for Dapr, whose template has no chart label, from the version of its images and its app version, which equals the chart version).

| Example | Releases | Chart | Version | Pinned in |
| --- | --- | --- | --- | --- |
| Meitrex | `content-`, `course-`, `flashcard-`, `media-`, `quiz-`, `reward-`, `skilllevel-`, `user-service-db` | `postgresql` | 16.7.17 | `version` of each `helm_release` in `deploymentModel/*.tf` |
| Meitrex | `keycloak` | `keycloak` | 24.7.7 | `deploymentModel/keycloak.tf` |
| Meitrex | `minio` | `minio` | 17.0.11 | `deploymentModel/media_service.tf` |
| Meitrex | `redis` | `redis` | 21.2.10 | `deploymentModel/dapr.tf` |
| Meitrex | `dapr` | `dapr` | 1.15.6 | `deploymentModel/dapr.tf` |
| Meitrex | `keel` | `keel` | 1.0.5 | `deploymentModel/keel.tf` |
| T2Store-Microservices | `mongo-cart`, `mongo-order` | `mongodb` | 16.5.29 | `--version` in `deploymentModel/azure-start.sh` |
| T2Store-Modulith | `mongo` | `mongodb` | 16.5.29 | `--version` in `deploymentModel/azure-start.sh` |

Since chart 24.7.7 rejects the custom Keycloak image of Meitrex unless insecure images are allowed, `deploymentModel/keycloak.tf` now sets `global.security.allowInsecureImages` to `true`, as the Meitrex repository does since its commit [`10b62e9`](https://github.com/MEITREX/infrastructure/commit/10b62e9).

## v1.1 Fix Schema Errors and Warnings

- **Meitrex**: The relation `dapr-sidecar-injector_ConnectsTo_graphql_gateway` targeted `graphql_gateway`, which is no component; the component is `gits-gateway` (type `graphql_gateway-SoftwareApplication`, image `ghcr.io/it-rex-platform/graphql_gateway`, defined in `deploymentModel/gateway.tf` like the other dapr-enabled services the injector connects to). The relation now targets `gits-gateway` and is named accordingly. Found by `check_edmm.py` and the comparison script of the LLM-transformation evaluation (2026-11-16). Metrics unchanged: the actual model contains no injector-to-gateway relation under either name, so the relation stays a false negative.
- **Meitrex**: The type `redis-DatabaseSystem` declared `REDIS_MASTER_HOST`, `REDIS_MASTER_PASSWORD_FILE`, and `REDIS_MASTER_PORT_NUMBER` as `required: true`, although only `redis-replicas` has these properties (the chart sets the master-connection variables on the replicas only); `redis-master` fell back to the defaults. The three definitions are now `required: false`. Found by `check_edmm.py` (2026-11-16, warnings). Metrics unchanged: type definitions are not scored, and the type names assigned to the components stay the same.
- **OTEL-Shop-Ansible**: The component type `adservice-SoftwareApplication` of the component `adservice` was not defined; instead, the type definition named `accountingservice-SoftwareApplication` contained adservice's property definitions (`service.name=adservice`, `AD_SERVICE_PORT`), so the accountingservice's `KAFKA_SERVICE_ADDR` was undeclared as well. The mislabeled definition is renamed to `adservice-SoftwareApplication`, and `accountingservice-SoftwareApplication` is added with the accountingservice's five properties (evidence: the `accountingservice` role of the deployment model and the component's properties; the OTEL-Shop-Kubernetes model declares `KAFKA_SERVICE_ADDR` for its accountingservice likewise). Found by `check_edmm.py` (2026-11-16). Metrics unchanged: component types enter the evaluation only through Q2, which compares the types assigned to components, and those are untouched.
- **OTEL-Shop-Terraform**: Four relations used the endpoint `prometheus-server`, which is no component; the component is `prometheus` (`resource "docker_container" "prometheus"` in `deploymentModel/main.tf`; jaeger's `--prometheus.server-url=http://prometheus:9090` and grafana's datasource `url: http://prometheus:9090` name it). The relations `jaeger_ConnectsTo_prometheus`, `otelcol_ConnectsTo_prometheus`, `prometheus_ConnectsTo_otelcol`, and `grafana_ConnectsTo_prometheus` now use the component name. Found by `check_edmm.py` and the comparison script of the LLM-transformation evaluation (2026-11-16). Metrics unchanged: the actual model contains none of the four relations under either name (it has no false positives), so they stay false negatives.
- **OTEL-Shop-Terraform**: The components `frontendproxy`, `jaeger`, `grafana`, and `otelcol` and their component types defined `ports.internal`, `ports.external`, `volumes.host_path`, and `volumes.container_path` more than once, because the Terraform resources repeat the `ports` and `volumes` blocks; the duplicate keys also lose which internal port or path belongs to which external one. The keys now carry the index of their block in `deploymentModel/main.tf`, as Terraform addresses repeated blocks (`ports.0.internal`, `volumes.1.host_path`, …): 36 renamed properties, 18 in the four components and 18 in their four types. Found by `check_edmm.py` (2026-11-16). Metrics unchanged: properties are not part of the precision, recall, and F1 of the evaluation.
- **OTEL-Shop-Terraform**: The type `productcatalogservice-SoftwareApplication` defined `MONGO_HOST`, but the component and the input define `MONGO_HOSTNAME` (`MONGO_HOSTNAME=mongo` in `deploymentModel/main.tf`), leaving the component's property undeclared. The property definition is renamed to `MONGO_HOSTNAME`. Found by `check_edmm.py` (2026-11-16). Metrics unchanged, as for the property fixes above.

With these fixes, `check_edmm.py` reports no errors and no warnings for any of the six models.
