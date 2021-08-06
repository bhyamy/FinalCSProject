from Manager.DecisionMaker.event import Event
from Manager.DecisionMaker.easyDecision import EasyDecision
from Manager.Processor.rawDataProcessor import RawDataProcessor
from Manager.cnfigs import UNITY_PORT, UNITY_IP, EEG_IP, EEG_PORT, PATH, UNITY_REQUEST, UNITY_BUFFER_SIZE, FORMAT
import csv, socket, time, threading

# event class test
test_data = [i for i in range(20)]
event_list = []
with open(PATH, newline='') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)
    for event in reader:
        event_list.append(Event(event))

for event in event_list:
    if event.should_be_activated(test_data):
        print(event.get_change())



def client_test_thread():
    time.sleep(5)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((UNITY_IP, UNITY_PORT))
    client.send(UNITY_REQUEST)
    response = client.recv(UNITY_BUFFER_SIZE)
    pairs_string = ''
    pairs_string += response.decode(FORMAT)
    print(pairs_string)


client_thread = threading.Thread(client_test_thread())
client_thread.start()

decision = EasyDecision(RawDataProcessor(), (UNITY_IP, UNITY_PORT), (EEG_IP, EEG_PORT), PATH)

print('done')
