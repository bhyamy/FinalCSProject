function TcpIpClientMatlabV1()
	%configure server%
	serverPort = 8080;                  % VR computer port
	serverIPAdress = '192.168.1.10';    % EEG-VR network IP
	%!configure server%

	%configure client%
	clientPort = 8888;            % the port that is configured in Actiview , default = 8888
	clientIPAdress = 'localhost'; % the ip adress of the pc that is running Actiview

	%variables%
	channels = 71;               % set to the same value as in Actiview "Channels sent by TCP" (64 EEG + 7 GSR)
	samples = 512;               % set to the same value as in Actiview "TCP samples/channel"
	words = channels*samples;
	run = true;
	requestSize = 1;
	msg_size = 9*words;          % subject to change depending on samples x channels
	timeout = 15;
	samples_channels = zeros(samples, channels); % every channel has a separate collumn
	%!variables

	%open tcp connection%
	%open server%
	tcpipServer = tcpip(serverIPAdress,serverPort,'NetworkRole','Server');
	set(tcpipServer,'InputBufferSize',requestSize);
	set(tcpipServer, 'OutputBufferSize', msg_size);
	set(tcpipServer,'Timeout',timeout);
	%!open server%

	%open client%
	tcpipClient = tcpip(clientIPAdress,clientPort,'NetworkRole','Client');
	set(tcpipClient,'InputBufferSize',msg_size);
	set(tcpipClient,'Timeout',timeout);
	%!open client%

	try
		fopen(tcpipServer);
	catch
		disp('Unable to open server connection');
		run = false;
	end
	try
		fopen(tcpipClient);
	catch
		disp('Actiview is unreachable please check if Actiview is running on the specified ip address and port number');
		run = false;
	end
	%!open tcp connection%

	while run
		% get request
		request = fread(tcpipServer, requestSize);
		
		if request == '1'
			% read tcp block
			[rawData, count, msg] = fread(tcpipClient, [3 words], 'uint8');
			if count ~= 3*words
				disp(msg);
				disp('Check ActiView Settings!');
				break
			end
			
			% reorder bytes from tcp stream into 32bit unsigned words
			normal_data = rawData(3,:)*(channels^3) + rawData(2,:)*(channels^2) + rawData(1,:)*channels;
			i = 0 : channels : words-1;
			
			for j = 1: channels;
				% the data structure of the samplesXchannels
				samples_channels(1:samples,j) = typecast(uint32(normal_data(i+j)), 'uint32');
			end
			str_data = mat2str(samples_channels);
			fwrite(tcpipServer, str_data);

		elseif request == '0'
			run = false;
			%cleanup%
			fclose(tcpipServer);
			delete(tcpipServer);
			fclose(tcpipClient);
			delete(tcpipClient);
			%!cleanup%
		end
end

end
