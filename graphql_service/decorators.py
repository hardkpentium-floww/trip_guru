
from typing import Dict

from structlog.contextvars import bind_contextvars

from graphql_service.utils import get_logger

log_error = get_logger(__name__).error


class Resolver:
    def __init__(self, split_resolver: Dict):
        self.split_resolver = split_resolver


class DataLoaderIdentifierAlreadyUsed(Exception):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name


class SplitIdentifierAlreadyUsed(Exception):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name


class Decorators:
    def __init__(self):
        self.query = {}
        self.mutation = {}
        self.dataloaders_cls_map = {}
        self.resolvers = Resolver(split_resolver={})

    def register_dataloader(self, cls_identifier):
        def decorator(cls_):
            registered_cls = self.dataloaders_cls_map.get(cls_identifier)
            if registered_cls:
                raise DataLoaderIdentifierAlreadyUsed(cls_identifier)
            self.dataloaders_cls_map[cls_identifier] = cls_

            def wrapper(*args, **kwargs):
                return cls_(*args, **kwargs)

        return decorator

    @property
    def register_resolver(self):
        def decorator(func):
            resolver = getattr(self.resolvers, func.__qualname__, None)
            if not resolver:
                setattr(self.resolvers, func.__qualname__, func)

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    @property
    def trace_batch_load_fn(self):
        def decorator(func):
            resolver = getattr(self.resolvers, func.__qualname__, None)
            if not resolver:
                setattr(self.resolvers, func.__qualname__, func)

            def wrapper(*args, **kwargs):

                import time

                start_time = time.time()
                response = func(*args, **kwargs)
                end_time = time.time()

                from graphql_service.utils.utils import snake_to_camel_case

                func_var = snake_to_camel_case(str(func.__module__))
                bind_contextvars(**{func_var: end_time - start_time})

                return response

            return wrapper

        return decorator

    def register_split_resolver(self, split_identifier: str):
        def decorator(func):
            resolver = self.resolvers.split_resolver.get(split_identifier)
            if not resolver:
                self.resolvers.split_resolver[split_identifier] = func
            else:
                raise SplitIdentifierAlreadyUsed(split_identifier)

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def register_query(self, operation_name: str, operation_value):
        def decorator(cls_):
            query = getattr(self.query, operation_name, None)
            if not query:
                setattr(self.query, operation_name, operation_value)

            def wrapper(*args, **kwargs):
                return cls_(*args, **kwargs)

            return wrapper

        return decorator

    def register_mutation(self, operation_name: str, operation_value):
        def decorator(cls_):
            query = getattr(self.mutation, operation_name, None)
            if not query:
                setattr(self.mutation, operation_name, operation_value)

            def wrapper(*args, **kwargs):
                return cls_(*args, **kwargs)

            return wrapper

        return decorator


decorators = Decorators()

register_query = decorators.register_query
register_mutation = decorators.register_mutation
register_dataloader = decorators.register_dataloader
register_resolver = decorators.register_resolver
register_split_resolver = decorators.register_split_resolver
resolvers = decorators.resolvers
trace_batch_load_fn = decorators.trace_batch_load_fn
