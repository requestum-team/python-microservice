from src.core.rpc.handlers import RPCHandler, RPCProgressHandler
from src.core.rpc.parsers import JsonParser
from src.core.utils.async_tools import progress_cb_decorator, thread_pool
from src.app.processing.rpc_example import rpc_task, rpc_task_with_progress


class RPCExample(RPCHandler):
    name = 'rpc-example-task'
    data_parser = JsonParser()

    def create_coroutine(self, data):
        return thread_pool(rpc_task)(data)


class RPCProgressExample(RPCProgressHandler):
    name = 'rpc-progress-example-task'
    data_parser = JsonParser()

    def create_coroutine(self, data, on_progress):
        return progress_cb_decorator(rpc_task_with_progress)(data, on_progress)

