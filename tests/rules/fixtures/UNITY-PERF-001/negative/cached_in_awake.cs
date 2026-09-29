using UnityEngine;

public class Mover : MonoBehaviour
{
    Rigidbody rb;
    Transform cam;
    void Awake()
    {
        rb = GetComponent<Rigidbody>();
        cam = Camera.main.transform;
    }
    void Update()
    {
        rb.AddForce(cam.forward);
    }
}
