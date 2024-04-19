import pytest
from ophyd_async.core import DeviceCollector

from p99Bluesky.devices.p99.sample_stage import SampleStage

# Long enough for multiple asyncio event loop cycles to run so
# all the tasks have a chance to run
A_BIT = 0.001


@pytest.fixture
async def sim_p99SampleStage():
    async with DeviceCollector(sim=True):
        sim_p99SampleStage = SampleStage("p99-MO-TABLE-01:", name="p99_stage")
        # Signals connected here

    yield sim_p99SampleStage


async def test_sim_p99SampleStage(sim_p99SampleStage: SampleStage) -> None:
    assert sim_p99SampleStage.name == "p99_stage"
