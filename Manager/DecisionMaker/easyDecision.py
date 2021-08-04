from Manager.DecisionMaker.decisionMaker import DecisionMaker
from Manager.DecisionMaker.event import Event
import csv



class EasyDecision(DecisionMaker):
    def __init__(self, processor, address, path):
        super(processor, address)
        self.event_list = self.__parse_events(path)

    # opens csv file to get events info.
    def __parse_events(self, path):
        event_list = []
        csv_file = open(path, newline='')
        reader = csv.reader(csv_file)
        for event in reader[1:]:
            event_list.append(Event(event))
        return event_list


    def analyze(self, processed_data):
        activated_events = []
        for event in self.event_list:
            if event.should_be_activated(processed_data):
                activated_events.append(event.get_change())
