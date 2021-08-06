from Manager.cnfigs import EEG_SAMPLING_RATE


class Event(object):
    """
    This is an event class representing an event occurring in the VR.

    Attributes
    ----------
    __range: tuple
        Range of frequencies (min_freq, max_freq)
    __threshold: float
        Positive float of desired threshold
    __name: str
        Name of speaker in VR
    __value: str
        String representation of the desired value for amplification of speaker.

    Methods
    ----------
        should_be_activated(processed data)
            Checks whether or not an event should be activated.
        get_change(processed_data)
            Returns the change that needs to occur if the event has happened.
    """
    def __init__(self, instruction):
        """
         Parameters
        ----------
        instruction : list
            A list of size 5 containing strings of:
                1. Minimum of range of frequencies
                2. Maximum of same
                3. Threshold the frequencies need to pass in order to activate event
                4. Name of the speaker the sound of which needs to be changed
                5. Float value of the required change to the speaker sound

        """
        freq_range, threshold, name, value = self.__parse_instruction(instruction)
        self.__range = freq_range
        self.__threshold = threshold
        self.__name = name
        self.__value = value

    @staticmethod
    def __parse_instruction(instruction):
        """Parses the instruction to an Event object.

        Parameters
        ----------
        path : str
            The path to the csv instructions file

        Returns
        ----------
        tuple
            A tuple of 4 elements representing the Event object.
        """
        min_range = int(instruction[0])
        max_range = int(instruction[1])
        threshold = float(instruction[2])
        name = instruction[3]
        value = max(0, min(float(instruction[4]), 1))
        return (min_range, max_range), threshold, name, value

    def should_be_activated(self, processed_data):
        """Checks whether or not an event has occurred.

            Parameters
            ----------
            processed_data : list
                List of max amplitudes of frequencies.

            Returns
            ----------
            bool
                True if max amplitude is above threshold, False otherwise.
        """
        for i in range(self.__range[0] * EEG_SAMPLING_RATE, self.__range[1] * EEG_SAMPLING_RATE + 1):
            if processed_data[i] > self.__threshold:
                return True
        return False

    def get_change(self):
        """Returns name of speaker to change his volume to volume * self.__value"""
        return self.__name, self.__value
