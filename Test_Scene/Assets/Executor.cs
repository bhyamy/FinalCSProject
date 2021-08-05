using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Executor : MonoBehaviour
{
    public Dictionary<string, float> valuesMap;
    [Range(0f, 1f)]
    public float volumeCheck1;
    [Range(0f, 1f)]
    public float volumeCheck2;
    public MyTCPClient client;

    private void Awake() {
        valuesMap = new Dictionary<string, float>();
    }
    // Start is called before the first frame update
    void Start()
    {
        client = new MyTCPClient("localhost", 5000);
    }

    // Update is called once per frame
    void Update()
    {
        UpdateValues();
    }

    void UpdateValues() {
        client.AskForData();
        while (!client.IsQEmpty())
        {
            var change = client.GetChange();
            valuesMap[change.Item1] = change.Item2;
        }
    }

    private void OnApplicationQuit() {
        client.Disconnect();
    }
}
