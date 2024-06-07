from softioc import builder


def soft_signal(prefix: str, input_name: str, readback_name: str) -> None:
    # Create some records
    builder.SetDeviceName(prefix)
    temp = builder.aIn(readback_name, initial_value=5)
    # rbv.append(temp)
    builder.aOut(
        input_name,
        initial_value=0.1,
        always_update=True,
        on_update=lambda v: temp.set(v),
    )
    # builder.device.ai.


"""
import asyncio

from softioc import asyncio_dispatcher, builder, softioc

# Create an asyncio dispatcher, the event loop is now running
dispatcher = asyncio_dispatcher.AsyncioDispatcher()

# Set the record prefix
builder.SetDeviceName("p99-motor")
# Create some records
ai = builder.aIn("AI", initial_value=5)
ao = builder.aOut(
    "AO", initial_value=0.1, always_update=True, on_update=lambda v: ao.set(v)
)

# Boilerplate get the IOC started
builder.LoadDatabase()
softioc.iocInit(dispatcher)


# Start processes required to be run after iocInit
async def update():
    while True:
        if abs(ai.get() - ao.get()) > 0.1:
            ai.set(ai.get() - (ai.get() - ao.get()) / 5.0)
            await asyncio.sleep(0.1)
        await asyncio.sleep(0.1)


dispatcher(update)

# Finally leave the IOC running with an interactive shell.
softioc.interactive_ioc(globals())


"""
