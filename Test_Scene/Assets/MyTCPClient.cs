using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;
 

public class MyTCPClient {
    private TcpClient socketConnection;
    private Thread clientReceiveThread;
	private ConcurrentQueue<(string, float)> q;

    // ctor
    public MyTCPClient(string ip, int port) {
        this.q = new ConcurrentQueue<(string, float)>();
		try
        {
            socketConnection = new TcpClient(ip, port);
			this.clientReceiveThread = new Thread(new ThreadStart(GetData));
			this.clientReceiveThread.IsBackground = true;
			this.clientReceiveThread.Start();
        }
        catch (SocketException socketException)
        {
            Debug.Log("Socket exception: " + socketException);
        }
		catch (ThreadAbortException threadAbortException)
		{
			Debug.Log("Thread abort exception: " + threadAbortException);
		}
        
    }
	
	public (string, float) GetChange() {
		(string, float) item;
		q.TryDequeue(out item);
		return item;
	}
	public bool IsQEmpty() {return q.IsEmpty;}
    private void GetData() {
        while (true) { 			 			
			Byte[] bytes = new Byte[1024];             
			try { 			

				// Get a stream object for reading 				
				using (NetworkStream stream = socketConnection.GetStream()) { 					
					int length; 					
					// Read incomming stream into byte arrary. 					
					while ((length = stream.Read(bytes, 0, bytes.Length)) != 0) { 					
						var incommingData = new byte[length]; 						
						Array.Copy(bytes, 0, incommingData, 0, length); 						
						// Convert byte array to string message. 						
						string serverMessage = Encoding.ASCII.GetString(incommingData);
						if (serverMessage.Equals("-")) continue; // if there are  no changes	 										
						Dictionary<string, float> values = StrToList(serverMessage);
						foreach(var key in values.Keys) {
							q.Enqueue((key, values[key]));
						}			
					} 				
				} 			
			}  catch (SocketException socketException) {             
			Debug.Log("Socket exception: " + socketException);         
			}  
			Thread.Sleep(1000);
		}           
    }

	private void SendMessage(string clientMessage) {
			if (socketConnection == null) {             
			return;         
		}  		
		try { 			
			// Get a stream object for writing. 			
			NetworkStream stream = socketConnection.GetStream(); 			
			if (stream.CanWrite) {                 				
				// Convert string message to byte array.                 
				byte[] clientMessageAsByteArray = Encoding.ASCII.GetBytes(clientMessage); 				
				// Write byte array to socketConnection stream.                 
				stream.Write(clientMessageAsByteArray, 0, clientMessageAsByteArray.Length);                 
				//Debug.Log("Client sent his message - should be received by server");             
			}         
		} 		
		catch (SocketException socketException) {             
			Debug.Log("Socket exception: " + socketException);         
		}  
	}

	public void Disconnect() {
		Debug.Log("terminating update thread");
		this.clientReceiveThread.Abort();
		Debug.Log("disconnecting from the server");
		SendMessage("0");
		this.socketConnection.Close();
	}

    private Dictionary<string, float> StrToList(string message) {
		Dictionary<string, float> map = new Dictionary<string, float>();
        List<string> result = new List<String>(message.Split(','));
		for (int i = 0; i < result.Count; i+=2)
		{
			map[result[i]] = float.Parse(result[i+1]);
		}
		return map;
    }

	public void AskForData() {
		SendMessage("1");
	}

	public void Pause() {
		this.clientReceiveThread.Suspend();
	}

	public void Continue() {
		this.clientReceiveThread.Resume();
	}
}

