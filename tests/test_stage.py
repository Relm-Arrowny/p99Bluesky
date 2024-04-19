import pytest
from ophyd_async.core import DeviceCollector

from p99Bluesky.devices.epics.set_read_only_motor import SetReadOnlyMotor


@pytest.fixture
async def sim_nc_motor():
    async with DeviceCollector(sim=True):
        sim_nc_motor = SetReadOnlyMotor("BLxx-MO-xx-01:")
        # Signals connected here

    yield sim_nc_motor


async def test_noConfigMortor(sim_nc_motor: SetReadOnlyMotor) -> None:
    assert sim_nc_motor.name == "sim_nc_motor"
