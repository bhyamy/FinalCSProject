from Processor import Processor
import numpy as np
from cnfigs import EEG_BUFFER_SIZE, EEG_GET_DATA_MSG, FORMAT


class FFTProcessor(Processor):
    """This is a FFT processor class implementing the Processor abstract class"""
    def __init__(self, ip, port):
        super(FFTProcessor, self).__init__(ip, port)

    def process(self):
        """Process incoming data using FFT to find max val of amplitude of frequencies"""
        self.client.send(EEG_GET_DATA_MSG)
        response = self.client.recv(EEG_BUFFER_SIZE)

        msg = ''
        msg += response.decode(FORMAT)
        data = np.mat(msg)
        # incoming is 512 (samples) X 71 (channels - 64 EEG + 7 GSR)
        # take EEG channels i.e. 1-64
        data = np.delete(data, np.s_[64:72], 1)
        fft = np.fft.fft2(data)
        
        self.processed_data = [max(row) for row in fft[1:]]
