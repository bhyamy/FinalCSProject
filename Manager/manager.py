from Manager.DecisionMaker.easyDecision import EasyDecision
from Manager.Processor.FFTProcessor import FFTProcessor
from Manager.Processor.rawDataProcessor import RawDataProcessor
from Manager.cnfigs import UNITY_IP, UNITY_PORT, EEG_IP, EEG_PORT, PATH
import time


def manage():
    decision_maker = EasyDecision(RawDataProcessor(), (UNITY_IP, UNITY_PORT), (EEG_IP, EEG_PORT), PATH)

    while decision_maker.is_unity_connected():
        decision_maker.take_decision()
        time.sleep(3)

    decision_maker.disconnect_from_eeg()


if __name__ == '__main__':
    manage()

