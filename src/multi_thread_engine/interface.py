# The idea of this module is to provide an external interface to objects that the client must use
from abc import ABC, abstractmethod
from queue import Queue
from dataclasses import dataclass
from typing import TypeVar, Generic
import threading
import logging

logging.basicConfig(level=logging.INFO)

from .config import *

# We use dataclass to enforce some attributes and ABC for method/strategy
@dataclass
class QueueObject(ABC):

    object_name: str
    object_type: str
    
    @abstractmethod
    def run(self) -> None:
        pass

T = TypeVar('T', bound=QueueObject)

class JobQueue(Queue[T], Generic[T]):
    def put(self, item: T, block: bool = True, timeout: float | None = None) -> None:
        if not isinstance(item, QueueObject):
            raise TypeError(f"Job must be a BaseJob, got {type(item).__name__}")
        super().put(item, block=block, timeout=timeout)

class WorkerPool(Generic[T]):
    def __init__(self, config: EngineConfig):
        self.queue: JobQueue[T] = JobQueue(**vars(config.queue_config))
        self.config = config

        for i in range(config.thread_config.worker_number):
            t = threading.Thread(target=self._worker, daemon=True, name=f"Worker-{i}")
            t.start()

    def _worker(self):
        while True:
            job: T = self.queue.get()
            try:
                job.run()
            finally:
                logging.info(f"Finished job {job.object_name}")
                self.queue.task_done()

    def submit(self, job: T) -> None:
        """Enqueue a job for processing."""
        self.queue.put(job)

    def join(self) -> None:
        """Block until all jobs are finished."""
        self.queue.join()

__all__ = ["QueueObject", "WorkerPool"]