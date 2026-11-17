resource "helm_release" "keel" {
  name       = "keel"
  repository = "https://charts.keel.sh"
  namespace  = kubernetes_namespace.gits.metadata[0].name
  chart      = "keel"
  version    = "1.0.5"

  set {
    name  = "helmProvider.enabled"
    value = "false"
  }
}
