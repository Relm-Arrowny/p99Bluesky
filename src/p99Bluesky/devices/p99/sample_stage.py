from ..stages import PitchRollStage, SelectableStage, ThetaStage, XYZRealwVirStage


class SampleStage(ThetaStage, PitchRollStage, XYZRealwVirStage, SelectableStage):
    def __init__(self, prefix: str, name: str):
        ThetaStage.__init__(self, prefix=prefix + "WRITE", name=name)
        PitchRollStage.__init__(self, prefix=prefix + "WRITE", name=name)
        XYZRealwVirStage.__init__(self, prefix=prefix, name=name, infix="Lab:")
        SelectableStage.__init__(self, prefix=prefix, name=name)
