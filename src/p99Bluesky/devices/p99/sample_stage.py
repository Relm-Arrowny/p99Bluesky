from ophyd_async.core import Device

from p99Bluesky.devices.epics.set_read_only_motor import SetReadOnlyMotor


class SampleAngleStage(Device):
    def __init__(self, prefix: str, name: str):
        self.theta = SetReadOnlyMotor(
            prefix, name, suffix=["WRITETHETA", "WRITETHETA:RBV", "WRITETHETA.EGU"]
        )
        self.roll = SetReadOnlyMotor(
            prefix, name, suffix=["WRITETHETA", "WRITETHETA:RBV", "WRITETHETA.EGU"]
        )
        self.pitch = SetReadOnlyMotor(
            prefix, name, suffix=["WRITETHETA", "WRITETHETA:RBV", "WRITETHETA.EGU"]
        )
        super().__init__(name=name)



