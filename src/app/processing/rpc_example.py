import time


def rpc_task_with_progress(data, progress):
    for i in range(5):
        time.sleep(1)
        progress(i/4)

    if data['success']:
        return data
    else:
        raise Exception(data)