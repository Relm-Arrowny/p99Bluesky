from enum import Enum

from ophyd_async.epics.areadetector.drivers.ad_base import ADBase
from ophyd_async.epics.areadetector.utils import ad_rw


class TriggerMode(str, Enum):
    internal = "Internal"
    ext_trigger = "External"
    ext_start = "External Start"
    ext_exposure = "External Exposure"
    ext_FVP = "External FVP"
    soft = "Software"


class Andor2Driver(ADBase):
    def __init__(self, prefix: str) -> None:
        self.trigger_mode = ad_rw(TriggerMode, prefix + "TriggerMode")
        super().__init__(prefix)
