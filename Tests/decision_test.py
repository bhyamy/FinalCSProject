from Manager.DecisionMaker.event import Event
from Manager.DecisionMaker.easyDecision import EasyDecision
from Manager.Processor.rawDataProcessor import RawDataProcessor
from Manager.cnfigs import UNITY_PORT, UNITY_IP, EEG_IP, EEG_PORT, PATH, UNITY_REQUEST, UNITY_BUFFER_SIZE, FORMAT
import csv, time

# event class test
test_data = [i for i in range(20)]
event_list = []
with open(PATH, newline='') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)
    for event in reader:
        event_list.append(Event(event))
csv_file.close()

for event in event_list:
    if event.should_be_activated(test_data):
        print(event.get_change())


decision = EasyDecision(RawDataProcessor(), (UNITY_IP, UNITY_PORT), (EEG_IP, EEG_PORT), PATH)
while decision.is_unity_connected():
    decision.take_decision()
    time.sleep(2)

decision.disconnect_from_eeg()

print('done')
