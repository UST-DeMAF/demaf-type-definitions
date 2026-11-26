# Examples

Each example consists of

- A technology-specific deployment model in `deploymentModel/`, which is taken from the source listed below,
- for examples that install Helm charts, the rendered templates of these charts in `helmTemplates/`, and
- the corresponding EDMM model (`*_edmm.yaml`), versioned in [CHANGELOG.md](CHANGELOG.md).

```text
<Example>/
├── deploymentModel/      technology-specific deployment model (input)
├── helmTemplates/        only for examples that install Helm charts
│   └── <release>.yaml    rendered templates of one Helm release (for reference)
└── <example>_edmm.yaml   EDMM model (output)
```

A deployment model refers to a Helm chart only by its name, so the Kubernetes resources that the chart creates are not part of the deployment model as plain-text files.
`helmTemplates/` contains these resources created by running `helm template` for the chart and the values that the deployment model sets.
They are stored here for reference purposes so that all parts of the EDMM model can be traced back to the technology-specific deployment model.

The deployment models are subject to the licenses of their sources listed below, not to the license of this repository.
The EDMM models and the TOSCA models in [winery](winery/) generated from them are licensed under the [Apache License 2.0](../LICENSE) of this repository.

| Example | Deployment Technologies | Deployment Model Source | Deployment Model License | Deployment Model Modifications | EDMM Model Source | EDMM Model Modifications |
| --- | --- | --- | --- | --- | --- | --- |
| [Meitrex](Meitrex/) | **Terraform**, Kubernetes, Helm, Docker | [MEITREX/infrastructure](https://github.com/MEITREX/infrastructure/tree/6fd6023e78e2f031241c2fdd21a2f87e0d5d85e9) at commit `6fd6023` | [MIT](Meitrex/deploymentModel/LICENSE) | `required_providers` block added to `main.tf` (as upstream did later in [`6cb99b4`](https://github.com/MEITREX/infrastructure/commit/6cb99b4)), Helm chart versions pinned, custom Keycloak image allowed in `keycloak.tf` | [v1](CHANGELOG.md) ([doi:10.5281/zenodo.15882026](https://doi.org/10.5281/zenodo.15882026)) | Relation target `graphql_gateway` corrected to `gits-gateway`, `REDIS_MASTER_*` properties of the type `redis-DatabaseSystem` made optional (v1.1), `ContainerPlatform` derived from `Platform`, type descriptions added (v1.4) |
| [OTEL-Shop-Ansible](OTEL-Shop-Ansible/) | **Ansible**, Docker | [`ansible/`](https://github.com/UST-DeMAF/opentelemetry-demo/tree/45a67dbc34d9bb247a19df80fea7d0cd6a246c82/ansible) of [UST-DeMAF/opentelemetry-demo](#ust-demafopentelemetry-demo) at commit `45a67db`, created by us | [Apache 2.0](https://github.com/UST-DeMAF/opentelemetry-demo/blob/45a67dbc34d9bb247a19df80fea7d0cd6a246c82/LICENSE) | Fixes and improvements in `main.yaml` and the roles (image references, role dependencies, environment variables), `README.md` reformatted, dependency of `loadgenerator` on `frontendproxy` removed (v1.4) | [v1](CHANGELOG.md) ([doi:10.5281/zenodo.15882026](https://doi.org/10.5281/zenodo.15882026)) | Type definitions of `adservice` and `accountingservice` corrected (v1.1), image of `productcatalogservice` corrected and `launchd` operations of `localhost` removed (v1.3), type descriptions added (v1.4) |
| [OTEL-Shop-Kubernetes](OTEL-Shop-Kubernetes/) | **Kubernetes**, Docker | [`kubernetes/opentelemetry-demo.yaml`](https://github.com/open-telemetry/opentelemetry-demo/blob/10048aa27eaf36304165b8ac1e9f61377a598b5b/kubernetes/opentelemetry-demo.yaml) of [open-telemetry/opentelemetry-demo](https://github.com/open-telemetry/opentelemetry-demo) at commit `10048aa` | [Apache 2.0](https://github.com/open-telemetry/opentelemetry-demo/blob/10048aa27eaf36304165b8ac1e9f61377a598b5b/LICENSE) | MongoDB added for the product catalog service (Deployment and Service `opentelemetry-demo-mongo`, `MONGO_*` variables and our image `ghcr.io/ust-demaf/demo:1.11.1-productcatalogservice` in `productcatalogservice`), quotes and whitespace normalized, as in [our fork](#ust-demafopentelemetry-demo) at commit `45a67db` | [v1](CHANGELOG.md) ([doi:10.5281/zenodo.15882026](https://doi.org/10.5281/zenodo.15882026)) | `ContainerPlatform` derived from `Platform`, type descriptions added (v1.4) |
| [OTEL-Shop-Terraform](OTEL-Shop-Terraform/) | **Terraform**, Docker | [`terraform/`](https://github.com/UST-DeMAF/opentelemetry-demo/tree/45a67dbc34d9bb247a19df80fea7d0cd6a246c82/terraform) of [UST-DeMAF/opentelemetry-demo](#ust-demafopentelemetry-demo) at commit `45a67db`, created by us | [Apache 2.0](https://github.com/UST-DeMAF/opentelemetry-demo/blob/45a67dbc34d9bb247a19df80fea7d0cd6a246c82/LICENSE) | External configuration files included in `files/`, fixes and improvements in `main.tf` (paths of these files, dependencies, environment variables), `README.md` reformatted, dependency of `loadgenerator` on `frontendproxy` removed and Windows paths in comments and `README.md` corrected (v1.4) | [v1](CHANGELOG.md) ([doi:10.5281/zenodo.15882026](https://doi.org/10.5281/zenodo.15882026)) | Relation endpoint `prometheus-server` corrected to `prometheus`, repeated `ports` and `volumes` properties indexed, property `MONGO_HOST` corrected to `MONGO_HOSTNAME` (v1.1), `ContainerPlatform` derived from `Platform`, type descriptions added (v1.4) |
| [T2Store-Microservices](T2Store-Microservices/) | **Bash**, Kubernetes, Helm, Terraform, Docker | `azure-start.sh` and `terraform/` of [Well5a/kube](#well5akube) at commit `7396499`, created by us; `k8/` from [`k8s/t2-microservices/base`](https://github.com/t2-project/devops/tree/729e3fa80da3aa859fb3c78103ea5e0dec8f0fd6/k8s/t2-microservices/base) of [t2-project/devops](https://github.com/t2-project/devops) at commit `729e3fa` | `azure-start.sh` and `terraform/`: [Apache 2.0](https://github.com/Well5a/kube/blob/73964997e577c08fdacb127085a94c80d280f111/LICENSE); `k8/`: not specified | Helm chart versions pinned in `azure-start.sh` | [v1](CHANGELOG.md) ([doi:10.5281/zenodo.15882026](https://doi.org/10.5281/zenodo.15882026)) | `ContainerPlatform` derived from `Platform`, property `resource_group_name` removed, type descriptions added (v1.4) |
| [T2Store-Modulith](T2Store-Modulith/) | **Bash**, Kubernetes, Helm, Terraform, Docker | `azure-start.sh` and `terraform/` of [Well5a/kube](#well5akube) at commit `7396499`, created by us; `k8/` from [`k8s/t2-modulith/base`](https://github.com/t2-project/devops/tree/729e3fa80da3aa859fb3c78103ea5e0dec8f0fd6/k8s/t2-modulith/base) of [t2-project/devops](https://github.com/t2-project/devops) at commit `729e3fa` | `azure-start.sh` and `terraform/`: [Apache 2.0](https://github.com/Well5a/kube/blob/73964997e577c08fdacb127085a94c80d280f111/LICENSE); `k8/`: not specified | `azure-start.sh` adapted to the modulith (one MongoDB release instead of `mongo-cart`, `mongo-order`, and `kafka`), Helm chart versions pinned in `azure-start.sh`, `image` line moved within the container of `k8/backend.yaml` | [v1](CHANGELOG.md) ([doi:10.5281/zenodo.15882026](https://doi.org/10.5281/zenodo.15882026)) | `ContainerPlatform` derived from `Platform`, property `resource_group_name` removed, type descriptions added (v1.4) |

The deployment technologies column lists all deployment technologies that an example uses. The technology in bold is the entry point: its deployment model embeds those of the other technologies.

The modifications of a deployment model refer to its source at the given commit. The modifications of an EDMM model refer to version v1, with the version that introduced them; [CHANGELOG.md](CHANGELOG.md) describes each of them. In addition, all EDMM models reference the EDMM YAML schema and state their version in their first lines since v1.1.

The TOSCA models in [winery](winery/) are generated from the EDMM models v1.4 with the visualization service of the DeMAF, to import and view them in [Eclipse Winery](https://github.com/eclipse/winery). Each example has its own namespace, named after the ID of the transformation process that generated it:

| Example | Namespace |
| --- | --- |
| [Meitrex](Meitrex/) | `fb331d9a-4d2c-4c1b-8558-d502ba85a050` |
| [OTEL-Shop-Ansible](OTEL-Shop-Ansible/) | `0c044fd9-e4b4-4d93-9237-df5eff650540` |
| [OTEL-Shop-Kubernetes](OTEL-Shop-Kubernetes/) | `367a5d58-e07f-4361-bb5d-ab4f2eadb479` |
| [OTEL-Shop-Terraform](OTEL-Shop-Terraform/) | `24b2fbf9-ff64-4030-b35e-66e5b597a01c` |
| [T2Store-Microservices](T2Store-Microservices/) | `0ec50331-bf06-41f7-9b18-2f560fcc0d22` |
| [T2Store-Modulith](T2Store-Modulith/) | `fe125fdc-1ee2-4785-8409-f6f5d3a4664d` |

## UST-DeMAF/opentelemetry-demo

[UST-DeMAF/opentelemetry-demo](https://github.com/UST-DeMAF/opentelemetry-demo) is our fork of [open-telemetry/opentelemetry-demo](https://github.com/open-telemetry/opentelemetry-demo) at commit [`10048aa`](https://github.com/open-telemetry/opentelemetry-demo/tree/10048aa27eaf36304165b8ac1e9f61377a598b5b) (20 commits after release 1.11.1).
In the fork, we extended the demo with a MongoDB for the product catalog service and created the Ansible and Terraform deployment models based on the Docker Compose deployment model of the demo (`docker-compose.yml`).

## Well5a/kube

[Well5a/kube](https://github.com/Well5a/kube/tree/73964997e577c08fdacb127085a94c80d280f111) is our fork of [t2-project/devops](https://github.com/t2-project/devops) at commit [`0a3155a`](https://github.com/t2-project/devops/tree/0a3155a), which contained only Kubernetes manifests.
In the fork, we created `azure-start.sh` and the Terraform files in `terraform/`: the script provisions an AKS cluster on Azure with Terraform, installs the Helm charts, and applies the Kubernetes manifests in `k8/`.
For the T2Store examples, we replaced these manifests of the fork, which date from 2021, with the current ones of t2-project/devops at commit [`729e3fa`](https://github.com/t2-project/devops/tree/729e3fa80da3aa859fb3c78103ea5e0dec8f0fd6), and kept the script and the Terraform files of the fork.
