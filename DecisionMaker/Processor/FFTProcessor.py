from Processor import Processor
import numpy as np
from cnfigs import EEG_BUFFER_SIZE, EEG_GET_DATA_MSG, FORMAT


class FFTProcessor(Processor):
    def __init__(self, ip, port):
        super().__init__(ip, port)

    def process(self):
        self.client.send(EEG_GET_DATA_MSG)
        response = self.client.recv(EEG_BUFFER_SIZE)

        msg = ''
        msg += response.decode(FORMAT)
        data = np.mat(msg)
        # incoming is 8 (samples) X 71 (channels - 64 EEG + 7 GSR)
        # take EEG channels i.e. 1-64
        data = np.delete(data, np.s_[64:72], 1)
        self.processed_data = np.fft.fft2(data)
