import time


def for_all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__:
            if attr.startswith("_"):
                continue
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate


def calculate_func_time(func):
    async def inner1(*args, **kwargs):
        begin = time.time()
        context = args[0].context
        context_key = args[0].context_key
        from structlog.contextvars import bind_contextvars

        result = await func(*args, **kwargs)
        end = time.time()
        exec_time = round((end - begin) * 1000, 3)
        context.exec_time += exec_time
        dict_ = {context_key: exec_time}
        bind_contextvars(**dict_)

        bind_contextvars(**dict_)
        return result

    return inner1


def calculate_method_time(func):
    def inner1(*args, **kwargs):
        from structlog.contextvars import bind_contextvars

        begin = time.time()

        result = func(*args, **kwargs)

        end = time.time()

        exec_time = round((end - begin) * 1000, 3)

        dict_ = {
            str("{}.{}".format(func.__module__, func.__qualname__)): exec_time
        }
        bind_contextvars(**dict_)

        return result

    return inner1
