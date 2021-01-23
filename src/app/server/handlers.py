from src.core.server.computation.handlers import ComputationTaskHandler
from src.core.server.computation.parsers import TextParser
from src.core.server.utils.async_tools import progress_cb_decorator
from src.app.processing.example import example_task_with_progress


class ExampleTask(ComputationTaskHandler):
    name = 'example-task'
    data_parser = TextParser()

    def create_coroutine(self, data, on_progress):
        return progress_cb_decorator(example_task_with_progress)(data, on_progress)

