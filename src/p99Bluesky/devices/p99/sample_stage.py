from ophyd_async.core import Device

from p99Bluesky.devices.stages import NoConfigMotor


class SampleStage(Device):
    def __init__(self, prefix: str, name: str):
        self.theta = NoConfigMotor(prefix, name, suffix="WRITETHETA")
        self.roll = NoConfigMotor(prefix, name, "WRITEROLL")
        super().__init__(name=name)


"""        PitchRollStage.__init__(self, prefix=prefix + "WRITE", name=name)
        self.pitch.setpoint = epics_signal_rw(float, prefix)
        self.roll.setpoint = epics_signal_rw(float, prefix)
        XYZRealwVirStage.__init__(self, prefix=prefix, name=name, infix="Lab:")
        self.x.setpoint = epics_signal_rw(float, prefix)
        self.y.setpoint = epics_signal_rw(float, prefix)
        self.z.setpoint = epics_signal_rw(float, prefix)
        self.virtualx.setpoint = epics_signal_rw(float, prefix)
        self.virtualy.setpoint = epics_signal_rw(float, prefix)
        self.virtualz.setpoint = epics_signal_rw(float, prefix)
        SelectableStage.__init__(self, prefix=prefix, name=name)
        self.select.setpoint = epics_signal_rw(float, prefix)"""
