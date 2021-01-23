import time


def example_task_with_progress(data, progress):
    for i in range(5):
        time.sleep(1)
        progress(i/4)

    return data