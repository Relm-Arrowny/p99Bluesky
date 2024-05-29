import pytest
from ophyd_async.core import DeviceCollector

from p99Bluesky.devices.stages import ThreeAxisStage


@pytest.fixture
async def mock_three_axis_motor():
    async with DeviceCollector(mock=True):
        mock_three_axis_motor = ThreeAxisStage("BLxx-MO-xx-01:", "mock_three_axis_motor")
        # Signals connected here

    yield mock_three_axis_motor


async def test_there_axis_motor(mock_three_axis_motor: ThreeAxisStage) -> None:
    assert mock_three_axis_motor.name == "mock_three_axis_motor"
    assert mock_three_axis_motor.x.name == "mock_three_axis_motor-x"
    assert mock_three_axis_motor.y.name == "mock_three_axis_motor-y"
    assert mock_three_axis_motor.z.name == "mock_three_axis_motor-z"
