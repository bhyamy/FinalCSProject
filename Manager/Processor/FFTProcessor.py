from Manager.Processor.processor import Processor
import numpy as np


class FFTProcessor(Processor):
    """This is a FFT processor class implementing the Processor abstract class.

    The processing here is made strictly on the first 64 channels (EEG).

    Methods
    ---------
        process(data)
            Process incoming data by using FFT.
    """
    def __init__(self):
        super().__init__()

    def process(self, data):
        """Process incoming data by using FFT.
        Data comes as string that is parsed as a matrix the an FFT is performed
        on the first 64 channels (of the EEG).

        Parameters:
            data: string
                A string representation of the recorded data from the EEG and GSR
        """
        data = np.mat(data)
        # delete channels 65-71 of the GSR
        data = np.delete(data, np.s_[64:72], 1)
        self.processed_data = np.fft.fft2(data)
