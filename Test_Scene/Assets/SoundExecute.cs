using UnityEngine;

public class SoundExecute : MonoBehaviour
{
    [Range(0f, 1f)]
    float value;
    public Executor executor;
    AudioSource source;

    // Start is called before the first frame update
    void Start()
    {
        source = transform.GetComponent<AudioSource>();
        executor.valuesMap[transform.name] = source.volume;
    }

    // Update is called once per frame
    void Update()
    {
        if (!executor.valuesMap.TryGetValue(transform.name, out value)) {
            Debug.Log("couldn't find object in map");
        }
        source.volume = value;
    }
}
