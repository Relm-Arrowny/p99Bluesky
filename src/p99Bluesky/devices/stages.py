from ophyd_async.core import Device
from ophyd_async.epics.motion.motor import Motor


class XYZStage(Device):
    def __init__(self, prefix: str, name: str):
        self.x = Motor(prefix + "X")
        self.y = Motor(prefix + "Y")
        self.z = Motor(prefix + "Z")
        Device.__init__(self, name=name)


class PitchRollStage(Device):
    def __init__(self, prefix: str, name: str):
        self.pitch = Motor(prefix + "PITCH")
        self.roll = Motor(prefix + "ROLL")
        Device.__init__(self, name=name)


class SelectableStage(Device):
    def __init__(self, prefix: str, name: str):
        self.select = Motor(prefix + "MP:SELECT")
        Device.__init__(self, name=name)


class ThetaStage(Device):
    def __init__(self, prefix: str, name: str):
        self.theta = Motor(prefix + "THETA")
        Device.__init__(self, name=name)


class XYZRealwVirStage(XYZStage):
    def __init__(self, prefix: str, name: str, infix: str):
        self.virtualx = Motor(prefix + infix + "X")
        self.virtualy = Motor(prefix + infix + "Y")
        self.virtualz = Motor(prefix + infix + "Z")
        XYZStage.__init__(self, prefix=prefix, name=name)
