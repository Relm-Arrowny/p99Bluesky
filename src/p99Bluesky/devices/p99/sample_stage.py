from ophyd_async.core import Device
from ophyd_async.epics.motion.motor import Motor
from ophyd_async.epics.signal.signal import epics_signal_rw


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


class ThetaStage(Device):
    def __init__(self, prefix: str, name: str):
        self.theta = P99Motor(prefix + "THETA")
        Device.__init__(self, name=name)


class XYZRealwVirStage(XYZStage):
    def __init__(self, prefix: str, name: str, infix: str):
        self.virtualx = P99Motor(prefix + infix + "X")
        self.virtualy = P99Motor(prefix + infix + "Y")
        self.virtualz = P99Motor(prefix + infix + "Z")
        XYZStage.__init__(self, prefix=prefix, name=name)


class SampleStage(ThetaStage, PitchRollStage, XYZRealwVirStage, SelectableStage):
    def __init__(self, prefix: str, name: str):
        ThetaStage.__init__(self, prefix=prefix + "WRITE", name=name)
        PitchRollStage.__init__(self, prefix=prefix + "WRITE", name=name)
        XYZRealwVirStage.__init__(self, prefix=prefix, name=name, infix="Lab:")
        SelectableStage.__init__(self, prefix=prefix, name=name)
