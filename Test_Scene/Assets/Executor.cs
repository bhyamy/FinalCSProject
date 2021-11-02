using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Executor : MonoBehaviour
{
    public Dictionary<string, float> valuesMap;
    public MyTCPClient client;

    private bool paused = false;

    private void Awake() {
        valuesMap = new Dictionary<string, float>();
    }
    // Start is called before the first frame update
    void Start()
    {
        client = new MyTCPClient("localhost", 5001);
    }

    // Update is called once per frame
    void Update()
    {
        if (!this.paused)
        {
            UpdateValues();
        }
    }

    void UpdateValues() {
        client.AskForData();
        while (!client.IsQEmpty())
        {
            var change = client.GetChange();
            //if (1) // checking if time of change is still relevent
            valuesMap[change.Item1] = change.Item2;
        }
    }

    private void OnApplicationQuit() {
        client.Disconnect();
    }

    public void Pause() {
        this.paused = true;
        this.client.Pause();
    }

    public void Continue() {
        this.paused = false;
        this.client.Continue();
    }
}
