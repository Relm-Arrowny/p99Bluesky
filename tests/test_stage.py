import pytest
from ophyd_async.core import DeviceCollector

from p99Bluesky.devices.p99.sample_stage import SampleStage

# Long enough for multiple asyncio event loop cycles to run so
# all the tasks have a chance to run
A_BIT = 0.001


@pytest.fixture
async def sim_p99SampleStage():
    async with DeviceCollector(sim=True):
        sim_p99SampleStage = SampleStage("p99-MO-TABLE-01:", "p99Stage")
        # Signals connected here

    assert sim_p99SampleStage.name == "p99Stage"
    yield sim_p99SampleStage


async def test_sim_p99SampleStage(sim_p99SampleStage: SampleStage) -> None:
    assert sim_p99SampleStage.theta.name == "p99Stage-theta"
    assert sim_p99SampleStage.pitch.name == "p99Stage-pitch"
    assert sim_p99SampleStage.roll.name == "p99Stage-roll"
    assert sim_p99SampleStage.x.name == "p99Stage-x"
    assert sim_p99SampleStage.y.name == "p99Stage-y"
    assert sim_p99SampleStage.z.name == "p99Stage-z"
    assert sim_p99SampleStage.virtualx.name == "p99Stage-virtualx"
    assert sim_p99SampleStage.virtualy.name == "p99Stage-virtualy"
    assert sim_p99SampleStage.virtualz.name == "p99Stage-virtualz"
