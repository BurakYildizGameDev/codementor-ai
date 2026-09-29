// EXPECT: 8, 9
using UnityEngine;

public class Aim : MonoBehaviour
{
    void LateUpdate()
    {
        if (TryGetComponent(out Rigidbody rb)) rb.Sleep();
        var forward = UnityEngine.Camera.main.transform.forward;
        transform.forward = forward;
    }
}
