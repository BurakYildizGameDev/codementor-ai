// EXPECT: 10
using UnityEngine;

public class Picker : MonoBehaviour
{
    public GameObject target;

    void Update()
    {
        if (target.tag == "Player")
        {
            Debug.Log("player");
        }
    }
}
