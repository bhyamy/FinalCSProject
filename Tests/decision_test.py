from Manager.DecisionMaker.event import Event
from Manager.DecisionMaker.easyDecision import EasyDecision
from Manager.Processor.FFTProcessor import FFTProcessor
from Manager.cnfigs import UNITY_PORT, UNITY_IP, EEG_IP, EEG_PORT, PATH


decision = EasyDecision(FFTProcessor(), (UNITY_IP, UNITY_PORT), (EEG_IP, EEG_PORT), PATH)





# checks event



print('done')
