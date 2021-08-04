from Manager.Processor.processor import Processor
import numpy as np
from Manager.cnfigs import EEG_BUFFER_SIZE, EEG_GET_DATA_MSG, FORMAT


class FFTProcessor(Processor):
    def __init__(self, ip, port):
        super().__init__(ip, port)

    def process(self):
        self.client.send(EEG_GET_DATA_MSG)
        response = self.client.recv(EEG_BUFFER_SIZE)

        data = ''
        data += response.decode(FORMAT)
        data = np.ndarray(data).reshape((64, 8))
        self.processed_data = np.fft.fft2(data)
