from Manager.Processor.processor import Processor
import numpy as np
from Manager.cnfigs import EEG_ELECTRODE_NUM, EEG_SAMPLING_NUM


class FFTProcessor(Processor):

    def process(self, data):
        data = np.ndarray(data).reshape((EEG_ELECTRODE_NUM, EEG_SAMPLING_NUM))
        self.processed_data = np.fft.fft2(data)
