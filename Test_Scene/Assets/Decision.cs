using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Decision : MonoBehaviour
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
        client = new MyTCPClient("localhost", 5002);
        client.GetData();
    }

    // Update is called once per frame
    void Update()
    {
        UpdateValues();
    }

    void UpdateValues() {
        while (!client.IsQEmpty())
        {
            var change = client.GetChange();
            valuesMap[change.Item1] = change.Item2;
        }
    }
}
