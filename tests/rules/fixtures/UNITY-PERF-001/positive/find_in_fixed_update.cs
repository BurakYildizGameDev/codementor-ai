// EXPECT: 8
using UnityEngine;

public class Follow : MonoBehaviour
{
    void FixedUpdate()
    {
        GameObject player = GameObject.Find("Player");
        transform.position = player.transform.position;
    }
}
