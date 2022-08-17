
class ServiceBase:
    def __init__(self, status) -> None:
        self.service_status = status if status \
            else {
                "config": {},
                "errors": []
            }

    def reset_status(self):
        self.service_status = {
            "config": {},
            "errors": []
        }

    @property
    def service_status(self): return self.service_status

    def __del__(self) -> None:
        self.service_status = None
