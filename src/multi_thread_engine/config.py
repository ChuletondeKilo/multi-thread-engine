# Here we create the entities that will store config data
# This configuration objects will be exposed to the client.
from dataclasses import dataclass, field


@dataclass
class ThreadPoolConfig:

    worker_number: int = field(default=3)

@dataclass
class QueueConfig:

    maxsize: int

@dataclass
class EngineConfig:

    thread_config: ThreadPoolConfig

__all__ = ["EngineConfig", "ThreadPoolConfig", "QueueConfig"]