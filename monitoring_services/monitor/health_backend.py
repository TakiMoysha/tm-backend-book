from health_check.backends import BaseHealthCheckBackend

class MyHealthCheckBackend(BaseHealthCheckBackend):
    critical_service = False

    def check_status(self):
        pass

    def identifier(self):
        return "MyHealthCheckBackend"
