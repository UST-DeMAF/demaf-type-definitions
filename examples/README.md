# Examples

Each example consists of

- a technology-specific deployment model in `deploymentModel/`, which is based on a third-party project, and
- the corresponding EDMM model (`*_edmm.yaml`) created with the DeMAF.

The deployment models are subject to the licenses of their source projects listed below, not to the license of this repository.
The EDMM models and the TOSCA models in [winery](winery/) generated from them were created with the DeMAF and are licensed under the [Apache License 2.0](../LICENSE) of this repository.

| Example | Deployment technology | Source | License | Modifications |
| --- | --- | --- | --- | --- |
| [Meitrex](Meitrex/) | Terraform | [MEITREX/infrastructure](https://github.com/MEITREX/infrastructure) | [MIT](Meitrex/deploymentModel/LICENSE) | Subset of the services, `main.tf` modified |
| [OTEL-Shop-Ansible](OTEL-Shop-Ansible/) | Ansible | [UST-DeMAF/opentelemetry-demo](https://github.com/UST-DeMAF/opentelemetry-demo/tree/main/ansible), fork of [open-telemetry/opentelemetry-demo](https://github.com/open-telemetry/opentelemetry-demo) | [Apache 2.0](https://github.com/open-telemetry/opentelemetry-demo/blob/main/LICENSE) | Modified |
| [OTEL-Shop-Kubernetes](OTEL-Shop-Kubernetes/) | Kubernetes | [open-telemetry/opentelemetry-demo](https://github.com/open-telemetry/opentelemetry-demo) | [Apache 2.0](https://github.com/open-telemetry/opentelemetry-demo/blob/main/LICENSE) | None |
| [OTEL-Shop-Terraform](OTEL-Shop-Terraform/) | Terraform | [UST-DeMAF/opentelemetry-demo](https://github.com/UST-DeMAF/opentelemetry-demo/tree/main/terraform), fork of [open-telemetry/opentelemetry-demo](https://github.com/open-telemetry/opentelemetry-demo) | [Apache 2.0](https://github.com/open-telemetry/opentelemetry-demo/blob/main/LICENSE) | `main.tf` and `README.md` modified |
| [T2Store-Microservices](T2Store-Microservices/) | Kubernetes, Terraform, Bash | [t2-project/devops](https://github.com/t2-project/devops) | Not specified | Terraform files and `azure-start.sh` modified |
| [T2Store-Modulith](T2Store-Modulith/) | Kubernetes, Terraform, Bash | [t2-project/devops](https://github.com/t2-project/devops) | Not specified | Terraform files, `azure-start.sh` and `k8/backend.yaml` modified |
