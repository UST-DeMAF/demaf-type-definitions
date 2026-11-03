# Examples

Each example consists of

- a technology-specific deployment model in `deploymentModel/`, which is taken from the source listed below, and
- the corresponding EDMM model (`*_edmm.yaml`) created with the DeMAF.

The deployment models are subject to the licenses of their sources listed below, not to the license of this repository.
The EDMM models and the TOSCA models in [winery](winery/) generated from them were created with the DeMAF and are licensed under the [Apache License 2.0](../LICENSE) of this repository.

| Example | Deployment technology | Source | License | Modifications |
| --- | --- | --- | --- | --- |
| [Meitrex](Meitrex/) | Terraform | [MEITREX/infrastructure](https://github.com/MEITREX/infrastructure/tree/6fd6023e78e2f031241c2fdd21a2f87e0d5d85e9) at commit `6fd6023` | [MIT](Meitrex/deploymentModel/LICENSE) | Subset of the services, `main.tf` modified |
| [OTEL-Shop-Ansible](OTEL-Shop-Ansible/) | Ansible | [`ansible/`](https://github.com/UST-DeMAF/opentelemetry-demo/tree/45a67dbc34d9bb247a19df80fea7d0cd6a246c82/ansible) of [UST-DeMAF/opentelemetry-demo](#ust-demafopentelemetry-demo) at commit `45a67db`, created by us | [Apache 2.0](https://github.com/UST-DeMAF/opentelemetry-demo/blob/45a67dbc34d9bb247a19df80fea7d0cd6a246c82/LICENSE) | Image references, role dependencies, and `README.md` modified |
| [OTEL-Shop-Kubernetes](OTEL-Shop-Kubernetes/) | Kubernetes | [`kubernetes/opentelemetry-demo.yaml`](https://github.com/UST-DeMAF/opentelemetry-demo/blob/45a67dbc34d9bb247a19df80fea7d0cd6a246c82/kubernetes/opentelemetry-demo.yaml) of [UST-DeMAF/opentelemetry-demo](#ust-demafopentelemetry-demo) at commit `45a67db`, extended by us with a MongoDB | [Apache 2.0](https://github.com/UST-DeMAF/opentelemetry-demo/blob/45a67dbc34d9bb247a19df80fea7d0cd6a246c82/LICENSE) | None |
| [OTEL-Shop-Terraform](OTEL-Shop-Terraform/) | Terraform | [`terraform/`](https://github.com/UST-DeMAF/opentelemetry-demo/tree/45a67dbc34d9bb247a19df80fea7d0cd6a246c82/terraform) of [UST-DeMAF/opentelemetry-demo](#ust-demafopentelemetry-demo) at commit `45a67db`, created by us | [Apache 2.0](https://github.com/UST-DeMAF/opentelemetry-demo/blob/45a67dbc34d9bb247a19df80fea7d0cd6a246c82/LICENSE) | Configuration files of `src/` included in `files/`, `main.tf` (paths of these files, dependencies) and `README.md` modified |
| [T2Store-Microservices](T2Store-Microservices/) | Kubernetes, Terraform, Bash | [t2-project/devops](https://github.com/t2-project/devops/tree/729e3fa80da3aa859fb3c78103ea5e0dec8f0fd6) at commit `729e3fa`, `k8/` from `k8s/t2-microservices/base` | Not specified | Terraform files and `azure-start.sh` modified |
| [T2Store-Modulith](T2Store-Modulith/) | Kubernetes, Terraform, Bash | [t2-project/devops](https://github.com/t2-project/devops/tree/729e3fa80da3aa859fb3c78103ea5e0dec8f0fd6) at commit `729e3fa`, `k8/` from `k8s/t2-modulith/base` | Not specified | Terraform files, `azure-start.sh` and `k8/backend.yaml` modified |

The modifications refer to the source at the given commit.

## UST-DeMAF/opentelemetry-demo

[UST-DeMAF/opentelemetry-demo](https://github.com/UST-DeMAF/opentelemetry-demo) is our fork of [open-telemetry/opentelemetry-demo](https://github.com/open-telemetry/opentelemetry-demo) at commit [`10048aa`](https://github.com/open-telemetry/opentelemetry-demo/tree/10048aa27eaf36304165b8ac1e9f61377a598b5b) (20 commits after release 1.11.1).
In the fork, we extended the demo with a MongoDB for the product catalog service and created the Ansible and Terraform deployment models based on the Kubernetes deployment model of the demo.
