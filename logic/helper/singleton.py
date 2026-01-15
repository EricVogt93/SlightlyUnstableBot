"""Singleton metaclass for ensuring single instance of a class."""
from typing import Any, Dict


class Singleton(type):
    """
    Metaclass that ensures only one instance of a class exists.

    Usage:
        class MyClass(metaclass=Singleton):
            pass
    """
    _instances: Dict[type, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def reset(mcs, cls: type) -> None:
        """Reset a singleton instance (useful for testing)."""
        if cls in mcs._instances:
            del mcs._instances[cls]
