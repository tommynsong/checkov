from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.kubernetes.checks.resource.base_spec_check import BaseK8Check

class ApiServerAuthorizationModeRBAC(BaseK8Check):
    def __init__(self):
        id = "CKV_K8S_77"
        name = "Ensure that the --authorization-mode argument includes RBAC"
        categories = [CheckCategories.KUBERNETES]
        supported_entities = ['containers']
        super().__init__(name=name, id=id, categories=categories, supported_entities=supported_entities)

    def get_resource_id(self, conf):
        return f'{conf["parent"]} - {conf["name"]}' if conf.get('name') else conf["parent"]

    def scan_spec_conf(self, conf):
        if conf.get("command") is not None:
            if "kube-apiserver" in conf["command"]:
                hasRBACAuthorizationMode = False
                for command in conf["command"]:
                    if command.startswith("--authorization-mode"):
                        modes = command.split("=")[1]
                        if "RBAC" in modes.split(","):
                            hasRBACAuthorizationMode = True
                return CheckResult.PASSED if hasRBACAuthorizationMode else CheckResult.FAILED
           
        return CheckResult.PASSED

check = ApiServerAuthorizationModeRBAC()