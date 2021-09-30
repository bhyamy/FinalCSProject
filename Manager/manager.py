from Manager.DecisionMaker.easyDecision import EasyDecision
from Manager.Processor.rawDataProcessor import RawDataProcessor
import time
import sys
from singletons import Logger, Config


def manage(confs):
    decision_maker = EasyDecision(
        RawDataProcessor(),
        (confs['UNITY']['IP'], confs['UNITY']['PORT']),
        (confs['EEG']['IP'], confs['EEG']['PORT']),
        confs['PATH'])

    while decision_maker.is_unity_connected():
        decision_maker.take_decision()
        time.sleep(3)

    decision_maker.disconnect_from_eeg()
    logger = Logger()
    logger.log()


if __name__ == '__main__':
    confs = Config()
    configured = False

    for arg in sys.argv:
        if '.yaml' in arg:
            configured = True
            confs.configure(sys.argv[1])
        break

    if not configured:
        confs.configure('default_configs.yaml')
    configurations = confs.configs
    manage(configurations)

