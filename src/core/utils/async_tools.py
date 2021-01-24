import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


process_pool_executor = ProcessPoolExecutor()
thread_pool_executor = ThreadPoolExecutor()


def thread_pool(f):
    async def wrapper(*args):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(thread_pool_executor, f, *args)

    return wrapper


def process_pool(f):
    async def wrapper(*args):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(process_pool_executor, f, *args)

    return wrapper


def progress_cb_decorator(fun, callback_param=None):
    """
    Decorates computation heavy function that has progress callback and makes it async.
    Decorator function can accepts async callback instead of sync one at the same position
    :param fun: function to decorate
    :param callback_param: index of callback argument, last argument by default
    :return: async decorator
    """

    async def wrapper(*args, **kwargs):
        def on_progress(value):
            nonlocal progress
            progress = value
            loop.call_soon_threadsafe(ev.set)

        def on_result(future: asyncio.Future):
            nonlocal result
            exception = future.exception()
            if exception:
                result = exception
            else:
                result = future.result()

            loop.call_soon_threadsafe(ev.set)

        # substitute progress callback
        index = len(args) - 1 if callback_param is None else callback_param
        async_callback = args[index]
        args = list(args)
        args[index] = on_progress
        args = tuple(args)

        # init variables and sync primitives
        ev = asyncio.Event()
        progress = 0
        result = None
        loop = asyncio.get_running_loop()

        # run task
        task = asyncio.create_task(thread_pool(fun)(*args, **kwargs))
        task.add_done_callback(on_result)

        # consume progress and result
        while True:
            await ev.wait()
            if result is not None:
                if isinstance(result, Exception):
                    raise result
                break

            await async_callback(progress)
            ev.clear()

        return result

    return wrapper
