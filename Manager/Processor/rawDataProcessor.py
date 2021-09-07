import numpy as np

from Manager.Processor.processor import Processor


class RawDataProcessor(Processor):
    """This is a raw data processor class implementing the Processor abstract class.
        Mainly used for testing

    Methods
    ---------
        process(data)
            Process incoming data by using FFT.
    """
    def __init__(self):
        super().__init__()

    def process(self, data):
        """Doesn't process Data. Returns the first vector of the given data as is.

        Parameters:
            data: string
                A string representation of the recorded data from the EEG and GSR
        """
        print('data in processor is:')
        print(data)
        self.processed_data = np.squeeze(np.asarray(data[0]))
