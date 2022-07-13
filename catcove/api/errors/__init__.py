from sanic.exceptions import (
    SanicException,
    NotFound
)

class CostumNotFound(NotFound):
    
    @property
    def message(self):
        ...
