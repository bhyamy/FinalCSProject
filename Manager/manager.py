from Manager.DecisionMaker.easyDecision import EasyDecision
import sys
from singletons import Logger, Config
from Manager.Processor.FFTProcessor import FFTProcessor
from Manager.Processor.rawDataProcessor import RawDataProcessor
import time


def process_factory(processor):
    if processor == 'raw_data':
        return RawDataProcessor()
    elif processor == 'FFT':
        return FFTProcessor()
    else:
        print('An unknown processor was given.')
        exit(1)


def decision_factory(decision_maker, processor, confs):
    if decision_maker == 'easy':
        return EasyDecision(process_factory(processor), (confs['UNITY']['IP'], confs['UNITY']['PORT']),
        (confs['EEG']['IP'], confs['EEG']['PORT']),
        confs['PATH'])
    else:
        print('An unknown decision maker was given.')
        exit(1)


def run(decision_maker, loop_time):
    while decision_maker.is_unity_connected():
        decision_maker.last_decision_time = time.time()
        decision_maker.take_decision()
        decision_sleep_time = loop_time - (time.time() - decision_maker.last_decision_time)
        time.sleep(decision_sleep_time if decision_sleep_time > 0 else 0)

    decision_maker.disconnect_from_eeg()


def manage(confs):
    decision_maker, processor, loop_time = confs['DECISION_MAKER'], confs['PROCESSOR'], confs['MANAGER']['DECISION_LOOP_TIME']
    logger = Logger()
    for _ in range(3):
        try:
            decision_maker = decision_factory(decision_maker, processor, confs)
            run(decision_maker, loop_time)
            break
        except ConnectionError as _:
            logger.print('manager got disconnected from EEG')
            logger.print('trying to reconnect...')
            time.sleep(5)
        except TimeoutError as _:
            logger.print('manager got disconnected from EEG')
            logger.print('trying to reconnect...')
            time.sleep(5)
        except Exception as e:
            logger.print('decision maker creation error')
            logger.print(e.with_traceback(e.__traceback__))
            break
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
    # TODO - add to .yaml decision maker and processor
    manage(configurations)
