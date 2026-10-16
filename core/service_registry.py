class ServiceRegistry:
    _services = {}

    @classmethod
    def register(cls, name, service):
        cls._services[name] = service

    @classmethod
    def get(cls, name):
        if name not in cls._services:
            raise KeyError(f"Service '{name}' is not registered")
        return cls._services[name]

    @classmethod
    def exists(cls, name):
        return name in cls._services

    @classmethod
    def unregister(cls, name):
        cls._services.pop(name, None)

    @classmethod
    def clear(cls):
        cls._services.clear()