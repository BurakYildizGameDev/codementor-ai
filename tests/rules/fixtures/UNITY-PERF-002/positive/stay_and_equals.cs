// EXPECT: 8, 14
using UnityEngine;

public class Hazard : MonoBehaviour
{
    void OnTriggerStay(Collider other)
    {
        if (other.gameObject.tag != "Enemy") return;
        Debug.Log("hasar");
    }

    void LateUpdate()
    {
        if (tag.Equals("Boss")) Debug.Log("boss");
    }
}
