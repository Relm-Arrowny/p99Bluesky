import asyncio
import subprocess

import pytest
from ophyd_async.core import DeviceCollector, set_mock_value

from p99_bluesky.devices.p99.sample_stage import (
    FilterMotor,
    SampleAngleStage,
    p99StageSelections,
)

# Long enough for multiple asyncio event loop cycles to run so
# all the tasks have a chance to run
A_BIT = 0.001


@pytest.fixture
async def mock_sampleAngleStage():
    async with DeviceCollector(mock=True):
        mock_sampleAngleStage = SampleAngleStage(
            "p99-MO-TABLE-01:", name="mock_sampleAngleStage"
        )
    yield mock_sampleAngleStage


@pytest.fixture
async def mock_filter_wheel():
    async with DeviceCollector(mock=True):
        mock_filter_wheel = FilterMotor("p99-MO-TABLE-01:", name="mock_filter_wheel")
    yield mock_filter_wheel


async def test_sampleAngleStage(mock_sampleAngleStage: SampleAngleStage) -> None:
    assert mock_sampleAngleStage.name == "mock_sampleAngleStage"
    assert mock_sampleAngleStage.theta.name == "mock_sampleAngleStage-theta"
    assert mock_sampleAngleStage.roll.name == "mock_sampleAngleStage-roll"
    assert mock_sampleAngleStage.pitch.name == "mock_sampleAngleStage-pitch"


async def test_filter_wheel(mock_filter_wheel: FilterMotor) -> None:
    assert mock_filter_wheel.name == "mock_filter_wheel"
    set_mock_value(mock_filter_wheel.user_setpoint, p99StageSelections.Cd25um)
    assert await mock_filter_wheel.user_setpoint.get_value() == p99StageSelections.Cd25um


async def test_soft_sampleAngleStage() -> None:
    p = subprocess.Popen(
        [
            "python",
            "tests/epics/soft_ioc/p99_softioc.py",
        ],
    )

    await asyncio.sleep(A_BIT)
    async with DeviceCollector(mock=False):
        mock_sampleAngleStage = SampleAngleStage(
            "p99-MO-TABLE-01:", name="mock_sampleAngleStage"
        )

    assert mock_sampleAngleStage.name == "mock_sampleAngleStage"
    assert mock_sampleAngleStage.theta.name == "mock_sampleAngleStage-theta"
    assert mock_sampleAngleStage.roll.name == "mock_sampleAngleStage-roll"
    assert mock_sampleAngleStage.pitch.name == "mock_sampleAngleStage-pitch"
    await asyncio.gather(
        mock_sampleAngleStage.theta.set(2),
        mock_sampleAngleStage.pitch.set(3.1),
        mock_sampleAngleStage.roll.set(4),
    )
    await asyncio.sleep(A_BIT)
    result = asyncio.gather(
        mock_sampleAngleStage.theta.get_value(),
        mock_sampleAngleStage.pitch.get_value(),
        mock_sampleAngleStage.roll.get_value(),
    )
    await asyncio.wait_for(result, timeout=2)
    assert result.result() == [2.0, 3.1, 4.0]

    p.terminate()
    p.wait()
