using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LightExecute : MonoBehaviour
{
    [Range(0f, 1f)]
    float value;
    public Executor executor;
    Light source;

    // Start is called before the first frame update
    void Start()
    {
        source = transform.GetComponent<Light>();
        executor.valuesMap[transform.name] = System.Convert.ToSingle(source.enabled);
    }

    // Update is called once per frame
    void Update()
    {
        if (!executor.valuesMap.TryGetValue(transform.name, out value)) {
            Debug.Log("couldn't find object in map");
        }
        source.enabled = System.Convert.ToBoolean(value);
    }
}
