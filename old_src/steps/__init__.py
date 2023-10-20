from .base_classes.base_step import BaseStep
from .processing_steps.mzmine3_batchmode import Mzmine3BatchMode
from .processing_steps.shrink_mgf import ShrinkMgf
from .processing_steps.sirius_fingerprint import SiriusFingerprint

steps: list[BaseStep] = []
steps.append(Mzmine3BatchMode)
steps.append(SiriusFingerprint)
steps.append(ShrinkMgf)
