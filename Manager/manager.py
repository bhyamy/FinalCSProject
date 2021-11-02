from Manager.DecisionMaker.easyDecision import EasyDecision
from Manager.Processor.FFTProcessor import FFTProcessor
from Manager.Processor.rawDataProcessor import RawDataProcessor
import Manager.cnfigs as c
import time


def process_factory(processor):
    if processor == 'raw_data':
        return RawDataProcessor()
    elif processor == 'FFT':
        return FFTProcessor()
    else:
        print('An unknown processor was given.')
        exit(1)


def decision_factory(decision_maker, processor):
    if decision_maker == 'easy':
        return EasyDecision(process_factory(processor), (c.UNITY_IP, c.UNITY_PORT), (c.EEG_IP, c.EEG_PORT), c.PATH)
    else:
        print('An unknown decision maker was given.')
        exit(1)


def run(decision_maker):
    while decision_maker.is_unity_connected():
        decision_maker.last_decision_time = time.time()
        decision_maker.take_decision()
        decision_sleep_time = c.DECISION_LOOP_TIME - (time.time() - decision_maker.last_decision_time)
        time.sleep(decision_sleep_time if decision_sleep_time > 0 else 0)

    decision_maker.disconnect_from_eeg()


def manage(decision_maker, processor):
    for _ in range(3):
        try:
            decision_maker = decision_factory(decision_maker, processor)
            run(decision_maker)
            break
        except ConnectionError as _:
            print('manager got disconnected from EEG')
            print('trying to reconnect...')
            time.sleep(5)
        except TimeoutError as _:
            print('manager got disconnected from EEG')
            print('trying to reconnect...')
            time.sleep(5)
        except Exception as e:
            print('decision maker creation error')
            print(e.with_traceback(e.__traceback__))
            break


if __name__ == '__main__':
    manage(c.DECISION_MAKER, c.PROCESSOR)
