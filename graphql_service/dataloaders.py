import time
from typing import Iterable, TypeVar

from aiodataloader import DataLoader

from graphql_service.context import Context
from graphql_service.decorators import trace_batch_load_fn
from graphql_service.utils.calculate_resolvers_time import calculate_func_time

K = TypeVar("K")
R = TypeVar("R")


class BaseDataLoader(DataLoader):
    context_key = None
    context = None

    def __new__(cls, context: Context):
        key = cls.context_key
        if key is None:
            raise TypeError(
                "Data loader %r does not define a context key" % (cls,)
            )
        if not hasattr(context, "dataloaders"):
            context.dataloaders = {}
        if key not in context.dataloaders:
            context.dataloaders[key] = super().__new__(cls)
        loader = context.dataloaders[key]
        assert isinstance(loader, cls)
        return loader

    def __init__(self, context):
        if self.context != context:
            self.context = context
            self.user_id = context.user_id
            super().__init__()

    @calculate_func_time
    def batch_load_fn(self, keys: Iterable[K]):
        start = time.time()
        value = self.batch_load(keys)
        end = time.time()
        exec_time = round((end - start) * 1000, 3)
        self.context.exec_time += exec_time
        return value

    @trace_batch_load_fn
    async def batch_load(self, keys: Iterable[K]):
        raise NotImplementedError()
