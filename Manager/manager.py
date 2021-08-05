from Manager.DecisionMaker.easyDecision import EasyDecision
from Manager.Processor.FFTProcessor import FFTProcessor
from Manager.cnfigs import UNITY_IP, UNITY_PORT, EEG_IP, EEG_PORT
import time


def manage():
    decision_maker = EasyDecision(FFTProcessor(), (UNITY_IP, UNITY_PORT), (EEG_IP, EEG_PORT))

    while decision_maker.is_connected():
        decision_maker.take_decision()
        time.sleep(1)

    decision_maker.disconnect_from_eeg()

if __name__ == '__main__':
    manage()
