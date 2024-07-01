import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp
from bluesky.preprocessors import (
    finalize_wrapper,
)
from ophyd_async.epics.motion import Motor
from ophyd_async.protocols import AsyncReadable

from p99_bluesky.log import LOGGER


def fast_scan(
    dets: list[AsyncReadable],
    motor: Motor,
    start: float,
    end: float,
    motor_speed: float | None = None,
):
    """
    Fast scan, where the motor moves to the starting point after which
      the motor is set in motion to toward the end point, during this movement detector
        are triggered and read out until the endpoint is reached or stopped.
    Note: This is purely software triggering which result in variable accuracy.
    However, fast scan does not require encoder and hardware setup and should
    work for all motor. It is most frequently use for alignment and
      slow motion measurements.

    Parameters
    ----------
    detectors : list
        list of 'readable' objects
    motor : Motor (moveable, readable) objcts

    start: float
        starting position.
    end: float,
        ending position

    motor_speed: Optional[float] = None,
        The speed of the motor during scan
    """

    # read the current speed and store it
    old_speed = yield from bps.rd(motor.velocity)

    @bpp.stage_decorator(dets)
    @bpp.run_decorator()
    def inner_fast_scan(
        dets: list[AsyncReadable],
        motor: Motor,
        start: float,
        end: float,
        motor_speed: float | None = None,
    ):
        yield from check_within_limit([start, end], motor)
        LOGGER.info(f"Moving {motor.name} to start position = {start}.")
        yield from bps.mv(motor, start)  # move to start

        if motor_speed:
            LOGGER.info(f"Set {motor.name} speed = {motor_speed}.")
            yield from bps.abs_set(motor.velocity, motor_speed)
        LOGGER.info(f"Set {motor.name} to end position({end}) and begin scan.")
        yield from bps.abs_set(motor.user_setpoint, end)
        current_value = yield from bps.rd(motor.user_readback)

        while abs(end - current_value) > 1e-5:
            yield from bps.trigger_and_read(dets + [motor])
            yield from bps.checkpoint()
            current_value = yield from bps.rd(motor.user_readback)

    yield from finalize_wrapper(
        plan=inner_fast_scan(dets, motor, start, end, motor_speed),
        final_plan=cleanUp(old_speed, motor),
    )


def check_within_limit(values: list, motor: Motor):
    LOGGER.info(f"Check {motor.name} limits.")
    lower_limit = yield from bps.rd(motor.low_limit_travel)
    high_limit = yield from bps.rd(motor.high_limit_travel)
    for value in values:
        if not lower_limit < value < high_limit:
            raise ValueError(
                f"{motor.name} move request of {value} is beyond limits:"
                f"{lower_limit} < {high_limit}"
            )


def cleanUp(old_speed, motor: Motor):
    LOGGER.info(f"Clean up: setting motor speed to {old_speed}.")
    if old_speed:
        yield from bps.abs_set(motor.velocity, old_speed)
