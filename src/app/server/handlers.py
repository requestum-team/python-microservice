from src.core.server.computation.handlers import ComputationTaskHandler
from src.core.server.computation.parsers import JsonParser
from src.core.server.utils.async_tools import progress_cb_decorator
from src.app.processing.computation_example import computation_task_with_progress


class ComputationExampleTask(ComputationTaskHandler):
    name = 'computation-example-task'
    data_parser = JsonParser()

    def create_coroutine(self, data, on_progress):
        return progress_cb_decorator(computation_task_with_progress)(data, on_progress)

