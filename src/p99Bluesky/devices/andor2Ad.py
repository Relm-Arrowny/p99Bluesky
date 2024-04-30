from collections.abc import Sequence

from bluesky.protocols import Hints
from ophyd_async.core import DirectoryProvider, SignalR, StandardDetector
from ophyd_async.epics.areadetector.drivers import ADBaseShapeProvider
from ophyd_async.epics.areadetector.writers import HDFWriter, NDFileHDF

from p99Bluesky.devices.epics.andor2_controller import Andor2Controller
from p99Bluesky.devices.epics.drivers.andor2_driver import Andor2Driver


class Andor2Ad(StandardDetector):
    _controller: Andor2Controller
    _writer: HDFWriter

    def __init__(
        self,
        prefix: str,
        directory_provider: DirectoryProvider,
        name: str,
        config_sigs: Sequence[SignalR] = (),
        **scalar_sigs: str,
    ):
        self.drv = Andor2Driver(prefix + "CAM:")
        self.hdf = NDFileHDF(prefix + "HDF5:")
        self.counter = 0

        super().__init__(
            Andor2Controller(self.drv),
            HDFWriter(
                self.hdf,
                directory_provider,
                self.filename,
                ADBaseShapeProvider(self.drv),
                sum="StatsTotal",
                **scalar_sigs,
            ),
            config_sigs=config_sigs,
            name=name,
        )

    def filename(self) -> str:
        self.counter += 1
        return self.name + str(self.counter)

    @property
    def hints(self) -> Hints:
        return self._writer.hints
