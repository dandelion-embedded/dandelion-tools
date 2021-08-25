import machine
import os
import ujson


def get_device_status() -> dict:
    return {
        "sysname": os.uname().sysname,
        "nodename": os.uname().nodename,
        "micropython-release": os.uname().release,
        "machine": os.uname().machine,
        "cpu_freq": machine.freq(),
        "reset_cause": machine.reset_cause(),
    }

print(ujson.dumps(get_device_status()))
