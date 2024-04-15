from ophyd_async.epics.signal.signal import epics_signal_rw

from p99Bluesky.devices.stages import (
    PitchRollStage,
    SelectableStage,
    ThetaStage,
    XYZRealwVirStage,
)

"""
class P99Motor(Motor):
    def __init__(self, prefix: str, name="") -> None:
        super().__init__(prefix, name)
        self.setpoint = epics_signal_rw(float, prefix)


class XYZStage(Device):
    def __init__(self, prefix: str, name: str):
        self.x = P99Motor(prefix + "X")
        self.y = P99Motor(prefix + "Y")
        self.z = P99Motor(prefix + "Z")
        Device.__init__(self, name=name)


class PitchRollStage(Device):
    def __init__(self, prefix: str, name: str):
        self.pitch = P99Motor(prefix + "PITCH")
        self.roll = P99Motor(prefix + "ROLL")
        Device.__init__(self, name=name)


class SelectableStage(Device):
    def __init__(self, prefix: str, name: str):
        self.select = P99Motor(prefix + "MP:SELECT")
        Device.__init__(self, name=name)


class XYZRealwVirStage(XYZStage):
    def __init__(self, prefix: str, name: str, infix: str):
        self.virtualx = P99Motor(prefix + infix + "X")
        self.virtualy = P99Motor(prefix + infix + "Y")
        self.virtualz = P99Motor(prefix + infix + "Z")
        XYZStage.__init__(self, prefix=prefix, name=name)

"""


class SampleStage(ThetaStage, PitchRollStage, XYZRealwVirStage, SelectableStage):
    def __init__(self, prefix: str, name: str):
        ThetaStage.__init__(self, prefix=prefix + "WRITE", name=name)
        self.theta.setpoint = epics_signal_rw(float, prefix)
        PitchRollStage.__init__(self, prefix=prefix + "WRITE", name=name)
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
        self.select.setpoint = epics_signal_rw(float, prefix)
