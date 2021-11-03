# FinalCSProject

## Installation Prerequisites
* Windows 7 and up
* python 2.x or 3.x
* Unity 2019.x or 2020.x


## Architecture
![alt text](https://github.com/bhyamy/FinalCSProject/blob/main/Project%20Architecture.jpeg)

### EEG data server
In order to be able to get data from the Actiview server in a diffrent computer by direct Ethernet cable (Athena - Venus**??) we had to create a relay server.
the EEG data server will get data from the Actiview and transfer it to the decision manager.
#### TCPIPClientServer.m file
```
normal_data = rawData(3,:)*(channels^3) + rawData(2,:)*(channels^2) + rawData(1,:)*channels;
```
Turns data received from Actiview server in 3 bytes to 2 bytes data, **ATTENTION** this might be wrong, this is how we were instructed
in the biosemi
forum to do it, also this is how the biosemi site delivered an example as to how to perform the conversion.
Additionally, the subsequent data is in microvolts.

Explanation on what the *while* loop does:
First a request is sent to the ActiView Server to get the data from the EEG or any other device connected to the biosemi, and then if
there was a problem
getting the data a message is displayed in the console where the .m file is running, then it concatenates the current time window to a
data structure that is
ultimately a 1 sec time frame of the neurological data recorded that is then sent through the server socket (tcpipServer) to the
machine running the VR.
When a disconnection request is sent the loop stops and cleans up the file pointers (server and client sockets).

### Decision manager


### Unity package

#### DecisionMaker class
In order for the BCI to work it is needed to implemnt in python a DecisionMaker sub-class implementing the abstract
method analyze() that receives as an argument processed data (more on that following), there is an example of how to
do that under the Manager/DecisionMaker folder (EasyDecision class), this method represents the way the processed data
is analyzed into decisions/actions in the VR environment.

#### Processing class
Another sub-class needed to be implemented is that of the Processor, similarly there is only one method needed to be
implemented which is the process() method that receives as input the raw data sent from the EEG computer.
This class represents the way the processing of the data is performed, there are 2 examples within the Manager/Processing
folder.

After implementing both abstract classes you need to add the appropriate lines in the manager.py file.


## Order Of Operations For Researchers
1. **After** placing the EEG on the subject open the AvtiView program in the EEG computer and go to the TCP Server tab, 
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
(If you have encountered any problems contact us at doramrani1010@gmail.com or bhyamy@gmail.com)

**If there is an executable:**
1. Execute Actiview.
2. **Before pressing start** define in the drop-down menu in the TCP-Server tab the number of channels that are connected (appears on the left).
3. Execute (double click on) the sever-client matlab file on same computer called TCPIPClientServer.
4. Run the python program with or without a configurations file (if not given a default one will be used), to run the program open the command line
and enter the following line "python manager.py ***configurations_file.yaml***" where the configurations_file.yaml contains the desired configurations for
the experiment.
5. Run VR environment (Unity).

**if there is no executable:**
1. Execute Actiview.
2. **Before pressing start** define in the drop-down menu in the TCP-Server tab the number of channels that are connected (appears on the left).
3. Double click the TCPIPClientServer.m file and press "Run".
4. Run the python program with or without a configurations file (if not given a default one will be used), to run the program open the command line
and enter the following line "python manager.py ***configurations_file.yaml***" where the configurations_file.yaml contains the desired configurations for
the experiment.
5. Run VR environment (Unity).

## Decision manager configuration
In order to configure all the relevent variables in the the Decision process we will use a .yaml file.

### How to create a .yaml confs file
For starters there is an example in the project called default_confs.yaml, there exists several sections in use currently in the
project such as [UNITY] - Unity communications configurations, [EEG] - communications confs for the machine delivering the real time data,
[FORMAT] - format of the messages sent and received through the network (normally don't use anything else) and probably the most useful one
for now is the [PATH] section that defines the path to the events file, more on that later on.
**ATTENTION** please notice that the configurations supplied do not contradict the hard-coded confs in the TCPIPClientServer.m file
because these confs cannot be changed during runtime.




## What is necessary in the machine running the VR experiment
On the machine running the VR experiment there is also a python program that, as mentioned earlier, should be activated after everything
in the data recording side had been completed (put EEG on subject, activate ActiView, run server...), where you should have also a
decision making and processing paradigms for the incoming data (e.g. FFT processor and a decision maker based off freq. amplitudes, neural network of some sort etc.).

### The aforementioned events file
As a basic decision making paradigm we have created an easyDecision class implementing the DecisionMaker abstract class (see DecisionMaker class instructions above),
what it does is get a path to a .csv file that contains conditions to the desired amplitudes, in the example the condition is to surpass a certain
threshold - which FFT is suitable for detecting.
The decisions are then sent to the Unity process as a list of tuples of *(object, value, time-stamp)*; *object* can be a sound/light source or anything similar, *value* is the desired value/change in value for the object based on the condition that was met and *time-stamp* is for verification.

As mentioned earlier to run the program perform one of the following:
1. Open the command line windows-key+r then type cmd and press enter, then run the command 'cd *ABSOLUTE_PATH_TO_FOLDER_CONTAINING_THE_PROGRAM*', unless the console is already in the folder, finally run the command mentioned above.
2. Go to the folder containing the program and at the top left side of the file explorer click the FILE tab and run the powershell (if the process won't run
normally run it as an administrator) the run the command mentioned above.

### Verbosity for error handling or data viewing
If you want to see the errors occurring or data transferred during runtime run the command with one of the following flags '-v' or '--verbose'.

## Logger
During runtime the data received and the decisions made are saved in a buffer that will be converted to a text file at the end of every experiment.
Please notice that it will be saved as *exp_time-CURRENT_DATE* even if the program collapsed.

###### Additional details
More information regarding the flow of the program, such as architechture and object relations, will be provided in a separate file.









