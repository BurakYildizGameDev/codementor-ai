using UnityEngine;

public class Picker : MonoBehaviour
{
    public GameObject target;

    void Update()
    {
        if (target.CompareTag("Player")) Debug.Log("player");
        if (target.name == "Player") Debug.Log("ad");
    }
}
