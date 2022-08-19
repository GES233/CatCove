
class ServiceBase:
    def __init__(self, status: None = None) -> None:
        if status:
            self.service_status = status
        else:
            self.service_status = {
                "config": {},
                "errors": []
            }

    def reset_status(self):
        self.service_status = {
            "config": {},
            "errors": []
        }

