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
