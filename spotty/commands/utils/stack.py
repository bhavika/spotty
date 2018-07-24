from time import sleep
from botocore.exceptions import EndpointConnectionError, WaiterError
from spotty.commands.writers.abstract_output_writrer import AbstractOutputWriter


def wait_for_status_changed(cf, stack_id, waiting_status, output: AbstractOutputWriter, delay=15):
    current_status = waiting_status
    stack = None
    while current_status == waiting_status:
        sleep(delay)
        try:
            res = cf.describe_stacks(StackName=stack_id)
        except EndpointConnectionError:
            output.write('Connection problem')
            continue

        stack = res['Stacks'][0]
        current_status = stack['StackStatus']

    return current_status, stack


def stack_exists(cf, stack_name):
    res = True
    try:
        cf.get_waiter('stack_exists').wait(StackName=stack_name, WaiterConfig={'MaxAttempts': 1})
    except WaiterError:
        res = False

    return res
