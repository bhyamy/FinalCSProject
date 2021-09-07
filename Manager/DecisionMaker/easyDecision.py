from Manager.DecisionMaker.decisionMaker import DecisionMaker
from Manager.DecisionMaker.event import Event
import csv


class EasyDecision(DecisionMaker):
    """
    This is a simple decision maker based on instructions given in a csv file.
    The file needs to have 5 columns:
        1st. Min frequency
        2nd. Max frequency (creating a range of frequencies)
        3rd. Threshold the frequencies (in the range) need to pass
        4th. Name of speaker in VR scene
        5th. Value of desired amplification of speaker sound ( > 0)

    ...

    Attributes
    ----------
    event_list: list
        Event objects parsed from csv file (instructions)

    Methods
    ----------
        __parse_events(path)
            Parses the instructions from the csv file to list of Event objects.
        analyze(processed_data)
            Analyzes whether or not to add an event to the list of activated event.
    """
    def __init__(self, processor, server_address, client_address, path):
        self.event_list = self.__parse_events(path)
        super(EasyDecision, self).__init__(processor, server_address, client_address)

    @staticmethod
    def __parse_events(path):
        """Parses the instructions from the csv file to list of Event objects.

        Opens the csv file and uses a reader to render iteratively all the
        instructions in it to Event objects.

        Parameters
        ----------
        path : str
            The path to the csv instructions file

        Returns
        ----------
        list
            A list of Event objects.
        """
        event_list = []
        with open(path, newline='') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for event in reader:
                event_list.append(Event(event))
        return event_list

    def analyze(self, processed_data):
        """Analyzes whether or not to add an event to the list of activated event.

            Opens the csv file and uses a reader to render iteratively all the
            instructions in it to Event objects.

            Parameters
            ----------
            processed_data : list
                List of amplitudes of frequencies.

            Returns
            ----------
            list
                A list of Event objects.
            """
        activated_events = []
        for event in self.event_list:
            if event.should_be_activated(processed_data):
                activated_events.append(event.get_change())
        return activated_events
