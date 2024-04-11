from dodal.beamlines.beamline_utils import device_instantiation
from dodal.beamlines.beamline_utils import set_beamline as set_utils_beamline
from dodal.log import set_beamline as set_log_beamline
from dodal.utils import get_beamline_name

from p99Bluesky.devices.p99.sample_stage import SampleStage

BL = get_beamline_name("p99")
set_log_beamline(BL)
set_utils_beamline(BL)


def sample_Stage(
    wait_for_connection: bool = True, fake_with_ophyd_sim: bool = False
) -> SampleStage:
    """Sample stage for p99"""

    return device_instantiation(
        SampleStage,
        prefix="-OP-PCHRO-01:TS:",
        name="turbo_slit",
        wait=wait_for_connection,
        fake=fake_with_ophyd_sim,
    )
