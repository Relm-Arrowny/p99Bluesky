import time

from softioc import asyncio_dispatcher, builder, softioc
from softsignal import soft_mbb, soft_motor, soft_signal


def p99_fake() -> None:
    # Sample AngleStage softioc
    dispatcher = asyncio_dispatcher.AsyncioDispatcher()
    soft_signal("p99-MO-TABLE-01", "WRITETHETA", "WRITETHETA:RBV")
    soft_signal("p99-MO-TABLE-01", "WRITEROLL", "WRITEROLL:RBV")
    soft_signal("p99-MO-TABLE-01", "WRITEPITCH", "WRITEPITCH:RBV")
    # sample selection staged
    soft_mbb("p99-MO-STAGE-02", "MP:SELECT")
    # xyz stage
    soft_motor(prefix="p99-MO-STAGE-02", name="X", unit="mm")
    soft_motor(prefix="p99-MO-STAGE-02", name="Y", unit="mm")
    soft_motor(prefix="p99-MO-STAGE-02", name="Z", unit="mm")
    # build the ioc
    builder.LoadDatabase()
    softioc.iocInit(dispatcher)
    # print(softioc.dbnr(), softioc.dbl())  # type: ignore
    while True:
        time.sleep(0.1)
    # softioc.interactive_ioc(globals())


if __name__ == "__main__":
    p99_fake()
