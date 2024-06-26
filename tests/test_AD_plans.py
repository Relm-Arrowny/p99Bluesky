from collections import defaultdict
from pathlib import Path
from unittest.mock import Mock

import pytest
from bluesky.plans import scan
from bluesky.run_engine import RunEngine
from bluesky.utils import new_uid
from ophyd.sim import SynAxis
from ophyd_async.core import (
    DeviceCollector,
    StaticDirectoryProvider,
    assert_emitted,
    callback_on_mock_put,
    set_mock_value,
)
from ophyd_async.epics.areadetector.drivers.ad_base import DetectorState

from p99_bluesky.devices.andor2Ad import Andor2Ad, Andor3Ad, StaticDirectoryProviderPlus
from p99_bluesky.plans.ad_plans import takeImg, tiggerImg

CURRENT_DIRECTORY = Path(__file__).parent
motor = SynAxis(name="motor")


async def make_andor2(prefix: str = "") -> Andor2Ad:
    dp = StaticDirectoryProviderPlus(CURRENT_DIRECTORY, "test-")

    async with DeviceCollector(mock=True):
        detector = Andor2Ad(prefix, dp, "andor2")
    return detector


@pytest.fixture
async def andor2() -> Andor2Ad:
    andor2 = await make_andor2(prefix="TEST")

    set_mock_value(andor2._controller.driver.array_size_x, 10)
    set_mock_value(andor2._controller.driver.array_size_y, 20)
    set_mock_value(andor2.hdf.file_path_exists, True)
    set_mock_value(andor2.hdf.num_captured, 0)
    set_mock_value(andor2.hdf.file_path, str(CURRENT_DIRECTORY))
    # assert "test-andor2-hdf0" == await andor2.hdf.file_name.get_value()
    set_mock_value(
        andor2.hdf.full_file_name, str(CURRENT_DIRECTORY) + "/test-andor2-hdf0"
    )
    return andor2


async def make_andor3(prefix: str = "test") -> Andor3Ad:
    dp = StaticDirectoryProvider(CURRENT_DIRECTORY, f"test-{new_uid()}")

    async with DeviceCollector(mock=True):
        andor3 = Andor3Ad(prefix, dp, "andor2")
    return andor3


async def test_Andor2(RE: RunEngine, andor2: Andor2Ad):
    docs = defaultdict(list)

    def capture_emitted(name, doc):
        docs[name].append(doc)

    RE.subscribe(capture_emitted)
    rbv_mocks = Mock()
    rbv_mocks.get.side_effect = [0, 3]
    callback_on_mock_put(
        andor2._writer.hdf.capture,
        lambda *_, **__: set_mock_value(andor2._writer.hdf.capture, value=True),
    )

    callback_on_mock_put(
        andor2.drv.acquire,
        lambda *_, **__: set_mock_value(andor2._writer.hdf.num_captured, rbv_mocks.get()),
    )

    RE(takeImg(andor2, 0.01, 3))
    assert_emitted(docs, start=1, descriptor=1, stream_resource=1, stream_datum=1, stop=1)
    # assert "" == docs


async def test_Andor2_tiggerImg(RE: RunEngine, andor2: Andor2Ad):
    docs = defaultdict(list)

    def capture_emitted(name, doc):
        docs[name].append(doc)

    RE.subscribe(capture_emitted)
    rbv_mocks = Mock()
    rbv_mocks.get.side_effect = range(0, 5)
    callback_on_mock_put(
        andor2._writer.hdf.capture,
        lambda *_, **__: set_mock_value(andor2._writer.hdf.capture, value=True),
    )

    callback_on_mock_put(
        andor2.drv.acquire,
        lambda *_, **__: set_mock_value(andor2._writer.hdf.num_captured, rbv_mocks.get()),
    )

    set_mock_value(andor2.drv.detector_state, DetectorState.Idle)

    RE(tiggerImg(andor2, 4))
    assert str(CURRENT_DIRECTORY) == await andor2.hdf.file_path.get_value()
    assert (
        str(CURRENT_DIRECTORY) + "/test-andor2-hdf0"
        == await andor2.hdf.full_file_name.get_value()
    )
    assert_emitted(
        docs, start=1, descriptor=1, stream_resource=1, stream_datum=1, event=1, stop=1
    )


async def test_Andor2_scan(RE: RunEngine, andor2: Andor2Ad):
    docs = defaultdict(list)

    def capture_emitted(name, doc):
        docs[name].append(doc)

    RE.subscribe(capture_emitted)
    rbv_mocks = Mock()
    rbv_mocks.get.side_effect = range(0, 100)
    mean_mocks = Mock()
    mean_mocks.get.side_effect = range(0, 120)
    callback_on_mock_put(
        andor2._writer.hdf.capture,
        lambda *_, **__: set_mock_value(andor2._writer.hdf.capture, value=True),
    )
    callback_on_mock_put(
        andor2.drv.acquire,
        lambda *_, **__: set_mock_value(andor2._writer.hdf.num_captured, rbv_mocks.get()),
    )
    callback_on_mock_put(
        andor2.drv.stat_mean,
        lambda *_, **__: set_mock_value(andor2.drv.stat_mean, mean_mocks.get()),
    )
    set_mock_value(andor2.drv.stat_mean, 50)
    set_mock_value(andor2.hdf.nd_array_address, 1234)
    set_mock_value(andor2.drv.detector_state, DetectorState.Idle)
    RE(scan([andor2], motor, -3, 3, 10))
    # RE(count([andor2], 3))
    assert str(CURRENT_DIRECTORY) == await andor2.hdf.file_path.get_value()
    assert (
        str(CURRENT_DIRECTORY) + "/test-andor2-hdf0"
        == await andor2.hdf.full_file_name.get_value()
    )
    assert_emitted(
        docs, start=1, descriptor=1, stream_resource=1, stream_datum=10, event=10, stop=1
    )
    # assert "" == docs
