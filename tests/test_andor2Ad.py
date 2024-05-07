from collections import defaultdict
from pathlib import Path, PosixPath

import pytest
from bluesky import plan_stubs as bps
from bluesky import preprocessors as bpp
from bluesky.run_engine import RunEngine
from bluesky.utils import new_uid, short_uid
from ophyd_async.core import (
    DetectorTrigger,
    DeviceCollector,
    StaticDirectoryProvider,
    TriggerInfo,
    assert_emitted,
    set_sim_value,
)
from ophyd_async.core._providers import DirectoryInfo

from p99Bluesky.devices.andor2Ad import Andor2Ad, StaticDirectoryProviderPlus

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
    single_detector = await make_detector(prefix="TEST")

    set_sim_value(single_detector._controller.driver.array_size_x, 10)
    set_sim_value(single_detector._controller.driver.array_size_y, 20)
    set_sim_value(single_detector.hdf.file_path_exists, True)
    set_sim_value(single_detector._writer.hdf.num_captured, 0)
    return single_detector


def takeImg(
    det: Andor2Ad,
    exposure: float,
    n_img: int,
    det_trig: DetectorTrigger,
):
    """Test plan to trigger the prepare part of the detect this is asynco/flyable."""
    grp = short_uid("prepare")
    tg = TriggerInfo(n_img, det_trig, exposure + 4, exposure)

    @bpp.stage_decorator([det])
    @bpp.run_decorator()
    def innerTakeImg():
        yield from bps.declare_stream(det, name="primary", collect=False)
        yield from bps.prepare(det, tg, group=grp, wait=True)
        yield from bps.kickoff(det, group=grp, wait=True)
        for n in range(1, n_img + 2):
            yield from bps.sleep(0.001)
            set_sim_value(det._writer.hdf.num_captured, n)
        yield from bps.complete(det, group=grp, wait=True)

    return (yield from innerTakeImg())


async def test_Andor(RE: RunEngine, single_detector: Andor2Ad):
    docs = defaultdict(list)

    def capture_emitted(name, doc):
        docs[name].append(doc)

    RE.subscribe(capture_emitted)
    RE(count_sim(single_detector))

    assert_emitted(
        docs, start=1, descriptor=1, stream_resource=2, stream_datum=2, event=1, stop=1
    )
    docs = defaultdict(list)
    RE(takeImg(single_detector, 0.2, 2, det_trig=DetectorTrigger.internal))
    # since it is external stream nothing comes back here
    assert_emitted(docs, start=1, descriptor=1, stop=1)


@pytest.fixture
def sim_staticDP(
    dir: Path = Path("/what/dir/"), filename_prefix: str = "p99"
) -> StaticDirectoryProviderPlus:
    sim_staticDP = StaticDirectoryProviderPlus(dir, filename_prefix)
    return sim_staticDP


def test_StaticDirectoryProviderPlus():
    dir: Path = Path("/what/dir/")
    filename_prefix: str = "p99"
    sim_staticDP = StaticDirectoryProviderPlus(dir, filename_prefix)
    assert sim_staticDP.__call__() == DirectoryInfo(
        root=Path("/what/dir/"), resource_dir=PosixPath("."), prefix="p99", suffix="0"
    )

    assert sim_staticDP.__call__() == DirectoryInfo(
        root=Path("/what/dir/"), resource_dir=PosixPath("."), prefix="p99", suffix="1"
    )
