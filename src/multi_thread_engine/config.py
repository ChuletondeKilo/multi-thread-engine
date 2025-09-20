# Here we create the entities that will store config data
# This configuration objects will be exposed to the client.
from dataclasses import dataclass, field

@dataclass
class Base:

    ...

class ThreadPoolConfig(Base):

    worker_number: int = field(default=3)


class QueueConfig(Base):

    ...


class EngineConfig(Base):

    thread_config: ThreadPoolConfig
    queue_config: QueueConfig

