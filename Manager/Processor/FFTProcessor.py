from Manager.Processor.processor import Processor
import numpy as np


class FFTProcessor(Processor):
    """
    This is a FFT processor class implementing the Processor abstract class.
    The processing here is made strictly on the first 64 channels (EEG).
    """
    def __init__(self, ip, port):
        super(FFTProcessor, self).__init__(ip, port)

    def process(self, data):
        data = np.mat(data)
        data = np.delete(data, np.s_[64:72], 1)
        self.processed_data = np.fft.fft2(data)
