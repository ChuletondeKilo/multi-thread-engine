# The idea of this module is to provide an external interface to objects that the client must use
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic
import logging
from concurrent.futures import ThreadPoolExecutor, Future, wait
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

class WorkerPool(Generic[T]):
    def __init__(self, config: EngineConfig):
        self.config: EngineConfig = config
        self.executor = ThreadPoolExecutor(
            max_workers=config.thread_config.worker_number,
            thread_name_prefix="Worker"
        )
        self.futures: list[Future] = []

    def submit(self, job: T) -> None:
        """Submit a job to the thread pool. Returns a Future."""

        if not isinstance(job, QueueObject):
            raise TypeError(f"Job must be a QueueObject, got {type(job).__name__}")

        def _wrapped():
            logging.info(f"Starting job {job.object_name}")
            try:
                return job.run()
            finally:
                logging.info(f"Finished job {job.object_name}")

        future = self.executor.submit(_wrapped)
        self.futures.append(future)
        return future

    def join(self) -> None:
        """Block until all submitted jobs are finished."""
        if self.futures:
            wait(self.futures)

    def shutdown(self, wait: bool = True) -> None:
        """Shut down the executor cleanly."""
        self.executor.shutdown(wait=wait)

    # --- context manager support ---
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.shutdown(wait=True)


__all__ = ["QueueObject", "WorkerPool"]