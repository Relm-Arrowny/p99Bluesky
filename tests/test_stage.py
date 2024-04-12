import pytest
from ophyd_async.core import DeviceCollector

from p99Bluesky.devices.stages import (
    PitchRollStage,
    SelectableStage,
    ThetaStage,
    XYZRealwVirStage,
)


class AllStages(ThetaStage, PitchRollStage, XYZRealwVirStage, SelectableStage):
    def __init__(self, prefix: str, name: str):
        ThetaStage.__init__(self, prefix=prefix, name=name)
        PitchRollStage.__init__(self, prefix=prefix, name=name)
        XYZRealwVirStage.__init__(self, prefix=prefix, name=name, infix="virtual:")
        SelectableStage.__init__(self, prefix=prefix, name=name)


@pytest.fixture
async def sim_all_stages():
    async with DeviceCollector(sim=True):
        sim_all_stages = AllStages("BLxx-MO-xx-01:", "Stages")
        # Signals connected here

    assert sim_all_stages.name == "Stages"
    yield sim_all_stages


async def test_sim_p99SampleStage(sim_all_stages: AllStages) -> None:
    assert sim_all_stages.theta.name == "Stages-theta"
    assert sim_all_stages.pitch.name == "Stages-pitch"
    assert sim_all_stages.roll.name == "Stages-roll"
    assert sim_all_stages.x.name == "Stages-x"
    assert sim_all_stages.y.name == "Stages-y"
    assert sim_all_stages.z.name == "Stages-z"
    assert sim_all_stages.virtualx.name == "Stages-virtualx"
    assert sim_all_stages.virtualy.name == "Stages-virtualy"
    assert sim_all_stages.virtualz.name == "Stages-virtualz"
