from ophyd_async.core import Device
from ophyd_async.epics.motion.motor import Motor

from p99Bluesky.devices.epics.NoConfigMotor import NoConfigMotor


class XYZStage(Device):
    """

    Standard ophyd_async xyz motor stage, by combining 3 Motors.

    Parameters
    ----------
    prefix:
        EPICS PV (None common part up to and including :).
    name:
        name for the stage.
    infix:
        EPICS PV, default is the ["X", "Y", "Z"].
    Notes
    -----
    Example usage::
        async with DeviceCollector():
        xyz_stage = XYZSTAGE("BLXX-MO-STAGE-XX:")

    """

    def __init__(self, prefix: str, name: str, infix: list[str] = None):
        if infix is None:
            infix = ["X", "Y", "Z"]
        self.x = Motor(prefix + infix[0])
        self.y = Motor(prefix + infix[1])
        self.z = Motor(prefix + infix[2])
        super().__init__(name=name)


class SingleBasicStage(Device):
    """

    Standard ophyd_async basic single stage, This stage contain only value and redback.
    This is quite common for example single piezo driver on mirrors.

    Parameters
    ----------
    prefix:
        EPICS PV (None common part up to and including :).
    name:
        name for the stage.
    infix:
        EEPICS PV, default is the [".VAL", ".RBV"].
    Notes
    -----
    Example usage::
        async with DeviceCollector():
        piezo1 = SingleBasicStage("BLXX-MO-STAGE-XX:")

    """

    def __init__(self, prefix: str, name: str, suffix: list[str] = None):
        if suffix is None:
            suffix = [".VAL", ".RBV"]
        self.stage = NoConfigMotor(prefix, name, suffix)
        super().__init__(name=name)
