from collections import defaultdict

import pytest
from bluesky import RunEngine
from bluesky import plan_stubs as bps
from bluesky.utils import new_uid
from ophyd_async.core import (
    DeviceCollector,
    StaticDirectoryProvider,
    assert_emitted,
    set_sim_value,
)

from p99Bluesky.devices.andor2Ad import Andor2Ad

CURRENT_DIRECTORY = "."  # str(Path(__file__).parent)


async def make_detector(prefix: str = "") -> Andor2Ad:
    dp = StaticDirectoryProvider(CURRENT_DIRECTORY, f"test-{new_uid()}")

    async with DeviceCollector(sim=True):
        detector = Andor2Ad(prefix, dp, "andor2")
    return detector


def count_sim(det: Andor2Ad, times: int = 1):
    """Test plan to do the equivalent of bp.count for a sim detector."""

    yield from bps.stage_all(det)
    yield from bps.open_run()
    yield from bps.declare_stream(det, name="primary", collect=False)
    for _ in range(times):
        read_value = yield from bps.rd(det._writer.hdf.num_captured)
        yield from bps.trigger(det, wait=False, group="wait_for_trigger")

        yield from bps.sleep(0.001)
        set_sim_value(det._writer.hdf.num_captured, read_value + 1)

        yield from bps.wait(group="wait_for_trigger")
        yield from bps.create()
        yield from bps.read(det)
        yield from bps.save()

    yield from bps.close_run()
    yield from bps.unstage_all(det)


@pytest.fixture
async def single_detector(RE: RunEngine) -> Andor2Ad:
    detector = await make_detector(prefix="TEST")

    set_sim_value(detector._controller.driver.array_size_x, 10)
    set_sim_value(detector._controller.driver.array_size_y, 20)
    set_sim_value(detector.hdf.file_path_exists, True)
    set_sim_value(detector._writer.hdf.num_captured, 0)
    # detector._intial_frame = 0
    # set_sim_value(detector.get_index, 0)
    # set_sim_value(detector._last_frame, 0)
    return detector


async def test_Andor(RE: RunEngine, single_detector: Andor2Ad):
    docs = defaultdict(list)

    def capture_emitted(name, doc):
        docs[name].append(doc)

    RE.subscribe(capture_emitted)

    RE(count_sim(single_detector))

    assert_emitted(
        docs, start=1, descriptor=1, stream_resource=2, stream_datum=2, event=1, stop=1
    )
    assert single_detector._controller.get_deadtime(0.2) == 0.2 + 0.1
