from Manager.DecisionMaker.easyDecision import EasyDecision
from Manager.Processor.FFTProcessor import FFTProcessor
from Manager.cnfigs import UNITY_IP, UNITY_PORT, EEG_IP, EEG_PORT
import time


def manage():
    processor = FFTProcessor(EEG_IP, EEG_PORT)
    decision_maker = EasyDecision(processor, (UNITY_IP, UNITY_PORT))

    while decision_maker.is_connected():
        decision_maker.take_decision()
        time.sleep(1)

    processor.disconnect()


if __name__ == '__main__':
    manage()
