from ophyd_async.core import Device
from ophyd_async.epics.motion.motor import Motor


class XYZStage(Device):
    def __init__(self, prefix: str, name: str):
        self.x = Motor(prefix=prefix + "X")
        self.y = Motor(prefix=prefix + "Y")
        self.z = Motor(prefix=prefix + "Z")
        super().__init__(name=name)


class PitchRollStage(Device):
    def __init__(self, prefix: str, name: str):
        self.pitch = Motor(prefix=prefix + "WRITEPITCH")
        self.roll = Motor(prefix=prefix + "WRITEROLL")
        super().__init__(name=name)


class SelectableStage(Device):
    def __init__(self, prefix: str, name: str):
        self.select = Motor(prefix=prefix + "MP:SELECT")
        super().__init__(name=name)


class thetaStage(Device):
    def __init__(self, prefix: str, name: str):
        self.select = Motor(prefix=prefix + "WRITETHETA")
        super().__init__(name=name)


class XYZRealwVirStage(XYZStage):
    def __init__(self, prefix: str, name: str):
        self.virtualx = Motor(prefix=prefix + "Lab:X")
        self.virtualy = Motor(prefix=prefix + "Lab:Y")
        self.virtualz = Motor(prefix=prefix + "Lab:Z")
        super().__init__(prefix=prefix, name=name)


class p99SampleStage(XYZRealwVirStage, thetaStage, PitchRollStage, SelectableStage):
    def __int__(self, prefix: str, name: str):
        super().__init__(prefix=prefix, name=name)
