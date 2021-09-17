# FinalCSProject

## Installation Prerequisites
* Windows 7 and up
* python 2.x or 3.x
* Unity 2019.x or 2020.x


## Decision And Processing Models For IT Technician.

### DecisionMaker class
In order for the BCI to work it is needed to implemnt in python a DecisionMaker sub-class implementing the abstract
method analyze() that receives as an argument processed data (more on that following), there is an example of how to
do that under the Manager/DecisionMaker folder (EasyDecision class), this method represents the way the processed data
is analyzed into decisions/actions in the VR environment.

### Processing class
Another sub-class needed to be implemented is that of the Processor, similarly there is only one method needed to be
implemented which is the process() method that receives as input the raw data sent from the EEG computer.
This class represents the way the processing of the data is performed, there are 2 examples within the Manager/Processing
folder.

After implementing both abstract classes you need to add the appropriate lines in the manager.py file.


## Order Of Operations For Researchers
1. **After*** placing the EEG on the subject open the AvtiView program in the EEG computer and go to the TCP Server tab, 
   click on the channels drop down menu and choose 64(EEG)+7(GSR).

**If the machine 'Athena' will be allowed to connect to the internet first follow these steps if not already done
(meaning if there is no executable file of the matlab client-server script):**
1. Double-click the file 'TcpIpClientMatlabV1'.
2. Run in the 'Command Window' the 'deploytool' command.
3. Select 'Application Compiler'.
4. Fill in Application Name, for example TCPIPClientServer (all of the rest is not necessary).
5. Press the *blue plus sign* next to 'Add main file' prompt.
6. Select file 'TcpIpClientMatlabV1'.
7. Select 'Package' button on the upper right corner of the window.
8. Wait until finished.
(If you have encountered any problems contact us at doramrani1010@gmail.com)

**If there is an executable**
2. Execute (double click on) the sever-client matlab file on same computer called TCPIPClientServer.
3. Run VR environment (Unity).
