import time

from softioc import asyncio_dispatcher, builder, softioc
from softsignal import soft_signal


def p99_fake_sample_angel_stage() -> None:
    # Sample AngleStage softioc
    dispatcher = asyncio_dispatcher.AsyncioDispatcher()
    builder.SetDeviceName("p99-MO-TABLE-01")
    soft_signal("p99-MO-TABLE-01", "WRITETHETA", "WRITETHETA:RBV")
    soft_signal("p99-MO-TABLE-01", "WRITEROLL", "WRITEROLL:RBV")
    soft_signal("p99-MO-TABLE-01", "WRITEPITCH", "WRITEPITCH:RBV")
    builder.LoadDatabase()
    softioc.iocInit(dispatcher)
    while True:
        time.sleep(0.1)


if __name__ == "__main__":
    p99_fake_sample_angel_stage()
