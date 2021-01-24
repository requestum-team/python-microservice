from src.core.rpc.handlers import RPCHandler
from src.core.rpc.parsers import JsonParser
from src.core.utils.async_tools import progress_cb_decorator
from src.app.processing.rpc_example import rpc_task_with_progress


class RPCExample(RPCHandler):
    name = 'rpc-example-task'
    data_parser = JsonParser()

    def create_coroutine(self, data, on_progress):
        return progress_cb_decorator(rpc_task_with_progress)(data, on_progress)

