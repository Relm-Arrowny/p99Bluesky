from unittest.mock import patch

import pytest
from ophyd_async.core import DetectorTrigger, DeviceCollector
from ophyd_async.epics.areadetector.controllers import (
    ADSimController,
)
from ophyd_async.epics.areadetector.drivers import ADBase
from ophyd_async.epics.areadetector.utils import ImageMode

from p99Bluesky.devices.epics.andor2_controller import Andor2Controller
from p99Bluesky.devices.epics.drivers.andor2_driver import Andor2Driver, TriggerMode


@pytest.fixture
async def pimte(RE) -> Andor2Controller:
    async with DeviceCollector(sim=True):
        drv = Andor2Driver("DRIVER:")
        controller = Andor2Controller(drv)

    return controller


@pytest.fixture
async def ad(RE) -> ADSimController:
    async with DeviceCollector(sim=True):
        drv = ADBase("DRIVER:")
        controller = ADSimController(drv)

    return controller


async def test_pimte_controller(RE, pimte: Andor2Controller):
    with patch("ophyd_async.core.signal.wait_for_value", return_value=None):
        await pimte.arm(num=1, exposure=0.002, trigger=DetectorTrigger.internal)

    driver = pimte.driver

    assert await driver.num_images.get_value() == 1
    assert await driver.image_mode.get_value() == ImageMode.multiple
    assert await driver.trigger_mode.get_value() == TriggerMode.internal
    assert await driver.acquire.get_value() is True
    assert await driver.acquire_time.get_value() == 0.002
    assert pimte.get_deadtime(2) == 2 + 0.1

    with patch(
        "ophyd_async.epics.areadetector.utils.wait_for_value", return_value=None
    ):
        await pimte.disarm()

    assert await driver.acquire.get_value() is False
