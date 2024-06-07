from softioc import asyncio_dispatcher, builder, softioc

from p99_bluesky.devices.epics.soft_ioc.softsignal import soft_signal

# Sample AngleStage softioc
dispatcher = asyncio_dispatcher.AsyncioDispatcher()
builder.SetDeviceName("p99-MO-TABLE-01")
soft_signal("p99-MO-TABLE-01", "WRITETHETA", "WRITETHETA:RBV")
soft_signal("p99-MO-TABLE-01", "WRITEROLL", "WRITEROLL:RBV")
soft_signal("p99-MO-TABLE-01", "WRITEPITCH", "WRITEPITCH:RBV")
builder.LoadDatabase()
softioc.iocInit(dispatcher)


softioc.interactive_ioc(globals())
