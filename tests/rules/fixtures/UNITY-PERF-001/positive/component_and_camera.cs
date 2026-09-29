// EXPECT: 8, 9
using UnityEngine;

public class Mover : MonoBehaviour
{
    void Update()
    {
        var rb = GetComponent<Rigidbody>();
        var cam = Camera.main.transform;
        rb.AddForce(cam.forward);
    }
}
