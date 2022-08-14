from .dev import DevConfig

class TestConfig(DevConfig):
    DEBUG: bool = False
    INSTANCE: bool = True
